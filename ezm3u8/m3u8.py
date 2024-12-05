import os
import re
from ezm3u8.channel import Channel
from ezm3u8.movie import Movie
from ezm3u8.tvshow import TVShow

import requests

movie_pattern = re.compile(r'(?P<network>.+) \((?P<title>\d{4})\) \((?P<year>\d{4})\)')
tv_pattern = re.compile(r'(?P<network>[^-]+) - (?P<title>.+) \((?P<year>\d{4})\) \((?P<country>[A-Z]{2})\) S(?P<season>\d{2}) E(?P<episode>\d{2})')
regular_channel_pattern = re.compile(r'(?P<COUNTRY>[A-Z]{2}) - (?P<TITLE>.+)')

class m3u8:
    
    def __init__(self, filepath: str | None = None, url: str | None = None):
        '''The function `__init__` initializes the M3U8 object with a default filepath.
        
        Parameters
        ----------
        filepath : str
            The `filepath` parameter is a string that represents the file path where the output will be saved. If no
        `filepath` is provided, the default value is set to the current directory (`"./"`).
        
        '''
        if filepath is None and url is None:
            raise ValueError("Either filepath or URL must be provided.")
        
        self.filepath = filepath
        self.url = url
        self.channels: list[Channel] = []
        self.movies: list[Movie] = []
        self.tv_shows: list[TVShow] = []
    
    def _parse_m3u8(self):
        '''The function `_parse_m3u8` reads or downloads the M3U8 file and extracts the channel, movie, and TV show information.
        
        '''
        if self.playlist:
            lines = self.playlist.split('\n')
        elif self.filepath:
            with open(self.filepath, 'r') as f:
                lines = f.readlines()
                self.playlist = "".join(lines)
        elif self.url:
            r = requests.get(self.url)
            lines = r.text.split('\n')
            self.playlist = r.text
            
        for line in lines:
            if line.startswith("#EXTINF:"):
                tvg_id = line.split("tvg-id=\"")[1].split("\"")[0]
                tvg_name = line.split("tvg-name=\"")[1].split("\"")[0]
                tvg_logo = line.split("tvg-logo=\"")[1].split("\"")[0]
                group_title = line.split("group-title=\"")[1].split("\"")[0]
                name = line.split(",")[1]
                url = lines[lines.index(line) + 1]
                print(tvg_id, tvg_name, tvg_logo, group_title, name, url)
                if match := re.match(movie_pattern, tvg_name):
                    self.movies.append(Movie(match['title'], match['year'], match['network'], url))
                if match := re.match(tv_pattern, tvg_name):
                    if not any(tv.title == match['title'] for tv in self.tv_shows):
                        self.tv_shows.append(TVShow(match['title'], match['network'], match['year'], match['country']))
                    tv_show = next(tv for tv in self.tv_shows if tv.title == match['title'])
                    tv_show.add_episode(int(match['season']), int(match['episode']), url)
                if match := re.match(regular_channel_pattern, tvg_name):
                    self.channels.append(Channel(match['TITLE'], match['COUNTRY'], url))
    
    def to_strm(self):
        '''
        The function `to_strm` converts the TV shows to .strm files.        
        '''
        if self.tv_shows:
            os.makedirs(f"./strm/tvshows", exist_ok=True)
        for tv_show in self.tv_shows:
            tv_show.to_strm(f"./strm/tvshows")
        
        if self.movies:
            os.makedirs(f"./strm/movies", exist_ok=True)
        for movie in self.movies:
            movie.to_strm(f"./strm/movies")
        
    def to_m3u8(self):
        '''The function `to_m3u8` converts the Channels to an M3U8 playlist.
        
        '''
        m3u8 = "#EXTM3U\n"
        for channel in self.channels:
            m3u8 += channel.to_m3u8() + "\n"
        return m3u8