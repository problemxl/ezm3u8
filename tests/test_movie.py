import pytest
from ezm3u8.movie import Movie

@pytest.fixture
def movie_instance():
    return Movie(title='Movie 1', year='2023', country='US', url='http://example.com/movie1')

def test_init(movie_instance):
    assert movie_instance.title == 'Movie 1'
    assert movie_instance.year == '2023'
    assert movie_instance.country == 'US'
    assert movie_instance.url == 'http://example.com/movie1'

def test_str(movie_instance):
    assert str(movie_instance) == 'Movie 1 (2023)'

def test_repr(movie_instance):
    assert repr(movie_instance) == 'Movie(title=Movie 1, year=2023, country=US, url=http://example.com/movie1)'

def test_to_strm(movie_instance, tmpdir):
    movie_instance.to_strm(filepath=tmpdir)
    strm_file = tmpdir.join('Movie 1.strm')
    with open(strm_file, 'r') as f:
        assert f.read() == 'http://example.com/movie1'