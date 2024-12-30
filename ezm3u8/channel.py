class Channel:

    def __init__(
        self,
        title: str,
        country: str,
        url: str,
        tvg_id: str = None,
        tvg_name: str = None,
        tvg_logo: str = None,
        group_title: str = None,
    ):
        """The function `__init__` initializes a Channel object with a title, country, and URL.

        Parameters
        ----------
        title : str
            The `title` parameter is a string that represents the title of the channel.
        country : str
            The `country` parameter is a string that represents the country of origin of the channel.
        url : str
            The `url` parameter is a string that represents the URL of the channel.

        """
        self.title: str = title
        self.country: str = country
        self.url: str = url

        self._tvg_id = tvg_id
        self._tvg_name = tvg_name
        self._tvg_logo = tvg_logo
        self._group_title = group_title

    def to_m3u8(self):
        """The function `to_m3u8` converts a Channel object to an M3U8 playlist entry."""

        return f'#EXTINF:-1 tvg-id="{self._tvg_id}" tvg-name="{self._tvg_name}" tvg-logo="{self._tvg_logo}" group-title="{self._group_title}",{self.title}\n{self.url}'

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Channel(title={self.title}, country={self.country}, url={self.url})"
