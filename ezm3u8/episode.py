import os


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
            # Remove trailing slash
            if filepath.endswith('/'):
                filepath = filepath[:-1]            
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            
            with open(f"{filepath}/{self.title} - S{self.season:02d}E{self.episode:02d}.strm", 'w') as f:
                f.write(self.url)
