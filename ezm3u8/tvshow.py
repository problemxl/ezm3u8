import os
from pathlib import Path

class Episode:
    
        def __init__(self, title, season, episode, url):
            self.title = title
            self.season = season
            self.episode = episode
            self.url = url
    
        def __str__(self):
            return f"{self.title} - S{self.season:02d}E{self.episode:02d}"
    
        def __repr__(self):
            return f"Episode(title={self.title}, season={self.season}, episode={self.episode}, url={self.url})"
        
        def to_strm(self, filepath: str = './'):
            '''The function `to_strm` sets a default filepath if none is provided.
            
            Parameters
            ----------
            filepath : str
                The `filepath` parameter is a string that represents the file path where the output will be saved. If no
            `filepath` is provided, the default value is set to the current directory (`"./"`).
            
            '''
            with open(f"{filepath}/{self.title} - S{self.season:02d}E{self.episode:02d}.strm", 'w') as f:
                f.write(self.url)
class TVShow:

    def __init__(self, title, network, year, country):
        self.title = title
        self.network = network
        self.year = year
        self.country = country
        self.seasons : dict[int, list[Episode]] = {}
        
    def add_episode(self, season, episode, url):
        if season not in self.seasons:
            self.seasons[season] = []
        self.seasons[season].append(Episode(self.title, season, episode, url))
        
    def __str__(self):
        return f"{self.title} ({self.year}) - {self.network} ({self.country})"
    
    def __repr__(self):
        return f"TVShow(title={self.title}, network={self.network}, year={self.year}, country={self.country})"
    
    def to_strm(self, filepath: str | Path = '.'):
        '''The function `to_strm` converts a TV show object to a list of .strm files.
        
        '''
        filepath = str(filepath)
        if filepath.endswith('/'):
            filepath = filepath[:-1]
        os.makedirs(f"{filepath}/{self.title}", exist_ok=True)
        for season, episodes in self.seasons.items():
            os.makedirs(f"{filepath}/{self.title}/Season {season:02d}", exist_ok=True)
            for episode in episodes:
                episode.to_strm(f"{filepath}/{self.title}/Season {season:02d}")
