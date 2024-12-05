import pytest
from ezm3u8.channel import Channel

@pytest.fixture
def channel_instance():
    return Channel(title='Channel 1', country='US', url='http://example.com/stream1')

def test_init(channel_instance):
    assert channel_instance.title == 'Channel 1'
    assert channel_instance.country == 'US'
    assert channel_instance.url == 'http://example.com/stream1'

def test_to_m3u8(channel_instance):
    m3u8_entry = channel_instance.to_m3u8()
    expected_entry = '#EXTINF:-1 tvg-id="Channel 1" tvg-name="Channel 1" tvg-logo="" group-title="US",Channel 1\nhttp://example.com/stream1'
    assert m3u8_entry == expected_entry

def test_str(channel_instance):
    assert str(channel_instance) == 'Channel 1'

def test_repr(channel_instance):
    assert repr(channel_instance) == 'Channel(title=Channel 1, country=US, url=http://example.com/stream1)'