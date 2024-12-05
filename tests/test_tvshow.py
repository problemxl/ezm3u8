import pytest
from ezm3u8.tvshow import TVShow, Episode

@pytest.fixture
def tvshow_instance():
    return TVShow(title='Show', network='Network', year=2023, country='US')

@pytest.fixture
def episode_instance():
    return Episode(title='Show', season=1, episode=1, url='http://example.com/episode1')

def test_tvshow_init(tvshow_instance):
    assert tvshow_instance.title == 'Show'
    assert tvshow_instance.network == 'Network'
    assert tvshow_instance.year == 2023
    assert tvshow_instance.country == 'US'

def test_add_episode(tvshow_instance, episode_instance):
    tvshow_instance.add_episode(season=1, episode=1, url='http://example.com/episode1')
    assert len(tvshow_instance.seasons[1]) == 1
    assert tvshow_instance.seasons[1][0].url == 'http://example.com/episode1'

def test_tvshow_str(tvshow_instance):
    assert str(tvshow_instance) == 'Show (2023) - Network (US)'

def test_tvshow_repr(tvshow_instance):
    assert repr(tvshow_instance) == 'TVShow(title=Show, network=Network, year=2023, country=US)'

def test_episode_init(episode_instance):
    assert episode_instance.title == 'Show'
    assert episode_instance.season == 1
    assert episode_instance.episode == 1
    assert episode_instance.url == 'http://example.com/episode1'

def test_episode_str(episode_instance):
    assert str(episode_instance) == 'Show - S01E01'

def test_episode_repr(episode_instance):
    assert repr(episode_instance) == 'Episode(title=Show, season=1, episode=1, url=http://example.com/episode1)'

def test_tvshow_to_strm(tvshow_instance, tmpdir):
    tvshow_instance.add_episode(season=1, episode=1, url='http://example.com/episode1')
    tvshow_instance.to_strm(filepath=tmpdir)
    strm_file = tmpdir.join('Show/Season 01/Show - S01E01.strm')
    with open(strm_file, 'r') as f:
        assert f.read() == 'http://example.com/episode1'

def test_episode_to_strm(episode_instance, tmpdir):
    episode_instance.to_strm(filepath=tmpdir)
    strm_file = tmpdir.join('Show - S01E01.strm')
    with open(strm_file, 'r') as f:
        assert f.read() == 'http://example.com/episode1'
        
def test_episode_to_stm_trailing_slash(episode_instance, tmpdir):
    episode_instance.to_strm(filepath=tmpdir + '/')
    strm_file = tmpdir.join('Show - S01E01.strm')
    with open(strm_file, 'r') as f:
        assert f.read() == 'http://example.com/episode1'