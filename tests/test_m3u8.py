import pytest
from ezm3u8.m3u8 import m3u8
from ezm3u8.channel import Channel
from ezm3u8.movie import Movie
from ezm3u8.tvshow import TVShow, Episode

@pytest.fixture
def m3u8_instance():
    return m3u8(url='http://ex.com/playlist.m3u8')

def test_init(m3u8_instance):
    assert m3u8_instance.url is not None
    assert m3u8_instance.filepath is None
    assert m3u8_instance.channels == []
    assert m3u8_instance.movies == []
    assert m3u8_instance.tv_shows == []

def test_parse_m3u8(m3u8_instance):
    m3u8_instance.playlist = "#EXTM3U\n#EXTINF:-1 tvg-id=\"1\" tvg-name=\"EX - Channel 1\" tvg-logo=\"\" group-title=\"Group 1\",Channel 1\nhttp://example.com/stream1\n"
    m3u8_instance._parse_m3u8()
    assert len(m3u8_instance.channels) == 1
    assert m3u8_instance.channels[0].title == 'Channel 1'

def test_to_strm(m3u8_instance, tmpdir):
    m3u8_instance.tv_shows = [TVShow(title='Show', network='Network', year=2023, country='US')]
    m3u8_instance.tv_shows[0].add_episode(season=1, episode=1, url='http://example.com/episode1')
    m3u8_instance.to_strm()
    # strm_file = tmpdir.join('./strm/tvshows/Show/Season 01/Show - S01E01.strm')
    with open('./strm/tvshows/Show/Season 01/Show - S01E01.strm', 'r') as f:
        assert f.read() == 'http://example.com/episode1'

def test_to_m3u8(m3u8_instance):
    m3u8_instance.channels = [Channel(title='Channel 1', country='US', url='http://example.com/stream1')]
    m3u8_content = m3u8_instance.to_m3u8()
    expected_content = '#EXTM3U\n#EXTINF:-1 tvg-id="Channel 1" tvg-name="Channel 1" tvg-logo="" group-title="US",Channel 1\nhttp://example.com/stream1\n'
    assert m3u8_content == expected_content