import os


class Movie:
    """The `Movie` class represents a movie entity with attributes such as title, year, and country."""

    def __init__(self, title: str, year: str, country: str, url: str):
        """The function defines an initializer method for a class with attributes for title, year, country, and URL.

        Parameters
        ----------
        title
            The `title` parameter in the `__init__` method is used to initialize the title of an object. It is typically a
        string that represents the title of a movie, book, song, or any other entity you are working with in your code.
        year
            The `year` parameter in the `__init__` method is used to store the year of release for a particular instance of the
        class. It is a part of the initialization process for creating objects of this class, allowing you to specify the
        year associated with a particular movie, book, or any
        country
            Country refers to the country of origin or production of the item being represented by the class. It could be the
        country where a movie was produced, where a book was published, or where a product was manufactured.

        """
        self.title: str = title
        self.year: str = year
        self.country: str = country
        self.url: str = url

    def __str__(self):
        return f"{self.title} ({self.year})"

    def __repr__(self):
        return f"Movie(title={self.title}, year={self.year}, country={self.country}, url={self.url})"

    def to_strm(self, filepath: str = './'):
        """The function `to_strm` converts a Movie object to a .strm file.

        Parameters
        ----------
        filepath : str
            The `filepath` parameter is a string that represents the file path where the output will be saved. If no
        `filepath` is provided, the default value is set to the current directory (`"./"`).

        """
        os.makedirs(filepath, exist_ok=True)
        with open(os.path.join(filepath, f"{self.title}.strm"), 'w') as f:
            f.write(self.url)