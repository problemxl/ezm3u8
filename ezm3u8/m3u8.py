import os
import re
from collections import defaultdict


from ezm3u8.channel import Channel
from ezm3u8.movie import Movie
from ezm3u8.tvshow import TVShow

import requests

movie_pattern = re.compile(r'(?P<network>.+?)\s*-\s*(?:(?P<id>\d+)\.\s*)?(?P<title>.+?)(?:\s*\((?P<year>\d{4})\))?$')
tv_pattern = re.compile(r'((?P<network>[^-]+)\s*-)?\s*(?P<title>.+) (\((?P<country>[A-Z]{2})\) )?S(?P<season>\d{2}) E(?P<episode>\d{2})')
regular_channel_pattern = re.compile(r'(?P<COUNTRY>.+?)\s*[-:]\s*(?P<TITLE>.+)')
# Check if string contains PPV or event
ppv_pattern = re.compile(r'PPV|Event|PPV Event|Pay-Per-View|PPV - | v |vs')

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
        self.playlist = None
        self.channels: dict[str, Channel] = {}
        self.tv_show_dict: dict[str, TVShow] = {}
        self.movies_dict: dict[str, Movie] = {}
        self.ppv_dict: dict[str, Channel] = {}
        self._parse_m3u8()
        print("Finished parsing M3U8 file")
    
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
            with open('playlist.m3u8', 'w') as f:
                f.write(r.text)
            
        for i in range(len(lines)):
            line = lines[i]
            if line.startswith("#EXTINF:"):
                # Extract information using a single split operation
                # tvg_id = line.split("tvg-id=\"")[1].split("\"")[0]
                tvg_name = line.split("tvg-name=\"")[1].split("\"")[0]
                # tvg_logo = line.split("tvg-logo=\"")[1].split("\"")[0]
                group_title = line.split("group-title=\"")[1].split("\"")[0]
                # name = line.split(",")[1]
                url = lines[i + 1].strip()

                if ppv_pattern.search(tvg_name):
                    self.ppv_dict[tvg_name] = Channel(tvg_name, "PPV", url)
                elif match := movie_pattern.match(tvg_name):
                    if has_extension(url):
                        self.movies_dict[tvg_name] = Movie(match['title'], match['year'], match['network'], url)
                elif match := tv_pattern.match(tvg_name):
                    if has_extension(url):
                        title = match['title']
                        if title not in self.tv_show_dict:
                            tv_show = TVShow(title, match['network'], country=match['country'])                        
                            self.tv_show_dict[title] = tv_show
                    self.tv_show_dict[title].add_episode(int(match['season']), int(match['episode']), url)
                elif match := regular_channel_pattern.match(tvg_name):
                    # print(f"Matched {tvg_name}")
                    # print(group_title)
                    if "UK" in group_title:
                        self.channels[tvg_name] = Channel(match['TITLE'], match['COUNTRY'], url)
                else:
                    print(f"Could not match {tvg_name}")
            # if i % 1000 == 0:
            #     print(f"Processed {i} lines")
    
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
        
    def to_m3u8(self, filepath: str = './playlist.m3u8'):
        '''The function `to_m3u8` converts the Channels to an M3U8 playlist.
        
        '''
        m3u8 = "#EXTM3U\n"
        for channel in self.channels.values():
            m3u8 += channel.to_m3u8() + "\n"
        with open(filepath, 'w') as f:
            f.write(m3u8)

def has_extension(url) -> bool:
    '''This function checks if a given URL has a file extension.
    
    Parameters
    ----------
    url
        A URL string that you want to check for the presence of a file extension.
    
    Returns
    -------
    bool
        A boolean value that indicates whether the URL has a file extension.
    '''
    return '.' in url.split('/')[-1]