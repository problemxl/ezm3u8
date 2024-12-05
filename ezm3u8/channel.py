class Channel:
    
    def __init__(self, title: str, country: str, url: str):
        '''The function `__init__` initializes a Channel object with a title, country, and URL.
        
        Parameters
        ----------
        title : str
            The `title` parameter is a string that represents the title of the channel.
        country : str
            The `country` parameter is a string that represents the country of origin of the channel.
        url : str
            The `url` parameter is a string that represents the URL of the channel.
        
        '''
        self.title: str = title
        self.country: str = country
        self.url: str = url
        
    def to_m3u8(self):
        '''The function `to_m3u8` converts a Channel object to an M3U8 playlist entry.
        
        '''
        # TODO: Fix the output format
        return f"#EXTINF:-1 tvg-id=\"{self.title}\" tvg-name=\"{self.title}\" tvg-logo=\"\" group-title=\"{self.country}\",{self.title}\n{self.url}"
    
    def __str__(self):
        return self.title
    
    def __repr__(self):
        return f"Channel(title={self.title}, country={self.country}, url={self.url})"