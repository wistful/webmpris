from django.test import TestCase
from django.test.client import Client
import json
from contextlib import nested
import mock
import webmpris


class PlayersTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_players(self):
        ids = [':1.235', '1:4589']
        with mock.patch('pympris.available_players', return_value=ids) as m:
            response = self.client.get('/webmpris/players')
            self.assertTrue(m.called)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, json.dumps(ids))


class BaseTestCase(object):

    """Base class to test webmpris REST API"""

    spec_props = None  # properties as a dict
    spec_props_changed = None  # changed properties

    CLS_VIEW = ''  # class name from the views module

    PATH = ''  # base url path to the REST API

    def setUp(self):
        self.client = Client()

    def test_get(self):
        spec = self.spec_props

        with nested(
            mock.patch('webmpris.views.check_player_id',
                       return_value=True)
        ):
            mymock = mock.Mock(**spec)
            setattr(getattr(webmpris.views, self.CLS_VIEW),
                    'CLS_MPRIS',
                    mock.Mock(return_value=mymock))
            url = '/webmpris/players/:TestPlayer/%s' % self.PATH
            response = self.client.get(url)
            self.assertEqual(json.loads(response.content), spec)

    def test_post(self):
        methods = getattr(getattr(webmpris.views, self.CLS_VIEW), 'methods')
        spec = {'{0}.return_value'.format(name): name for name in methods}
        with nested(
            mock.patch('webmpris.views.check_player_id',
                       return_value=True)
        ):
            mymock = mock.Mock(**spec)
            setattr(getattr(webmpris.views, self.CLS_VIEW),
                    'CLS_MPRIS',
                    mock.Mock(return_value=mymock))
            args = ['value1', 2, True]
            data = {'args': args}
            for method in methods:
                url = '/webmpris/players/:TestPlayer/%s/%s' % (
                    self.PATH, method)
                response = self.client.post(url,
                                            data=json.dumps(data),
                                            content_type="application/json")
                self.assertEqual(
                    json.loads(response.content).get('status'), 'success')
                self.assertTrue(getattr(mymock, method).called)
                getattr(mymock, method).assert_called_with(*args)

    def test_post_fail(self):
        methods = ('unknown_method', 'other_bad_method')
        spec = {'{0}.return_value'.format(name): name for name in methods}
        with nested(
            mock.patch('webmpris.views.check_player_id',
                       return_value=True)
        ):
            mymock = mock.Mock(**spec)
            setattr(getattr(webmpris.views, self.CLS_VIEW),
                    'CLS_MPRIS',
                    mock.Mock(return_value=mymock))
            args = {'args': ['value1', 2, True]}
            for method in methods:
                url = '/webmpris/players/:TestPlayer/%s/%s' % (
                    self.PATH, method)
                response = self.client.post(url,
                                            data=json.dumps(args),
                                            content_type="application/json")
                self.assertEqual(
                    json.loads(response.content).get('status'), 'fail')
                self.assertFalse(getattr(mymock, method).called)

    def test_put(self):
        spec = self.spec_props
        # actually this values are read-only
        # and can't be changed using pympris;
        # but we test webmpris, not pympris.
        spec2 = self.spec_props_changed

        with nested(
            mock.patch('webmpris.views.check_player_id',
                       return_value=True)
        ):
            mymock = mock.Mock(**spec)
            setattr(getattr(webmpris.views, self.CLS_VIEW),
                    'CLS_MPRIS',
                    mock.Mock(return_value=mymock))
            data = json.dumps(spec2)
            url = '/webmpris/players/:TestPlayer/%s' % self.PATH
            response = self.client.put(url, data=data,
                                       content_type="application/json")
            self.assertEqual(response.status_code, 200)
            resp_obj = json.loads(response.content)
            self.assertEqual(len(resp_obj.get('errmsg', [])), 0)

            # check values
            for key, value in spec2.items():
                self.assertEqual(getattr(mymock, key), value)


class RootTestCase(TestCase, BaseTestCase):

    spec_props = {
        'CanQuit': True,
        'Fullscreen': True,
        'CanSetFullscreen': True,
        'CanRaise': True,
        'HasTrackList': True,
        'Identity': 'TestIdentity',
        'DesktopEntry': 'test_entry',
        'SupportedUriSchemes': ['uri1', 'uri2'],
        'SupportedMimeTypes': ['mime1', 'mime2']
    }
    spec_props_changed = {
        'CanQuit': False,
        'HasTrackList': False,
        'Identity': 'OtherIdentity',
        'DesktopEntry': 'other_entry',
        'SupportedUriSchemes': ['new_uri1', 'new_uri2'],
        'SupportedMimeTypes': ['new_mime1', 'new_mime2']
    }

    CLS_VIEW = 'Root'
    PATH = 'Root'


class PlayerTestCase(TestCase, BaseTestCase):

    spec_props = {
        'PlaybackStatus': 'Stopped',
        'LoopStatus': 'Track',
        'Rate': 1,
        'Shuffle': True,
        'Metadata': {"mpris:trackid": "/org/mpris/MediaPlayer2/Track/1",
                     "xesam:url": "jazzradio://vocallegends"},
        'Volume': 0.20,
        'Position': 15000,
        'Minimumrate': 0,
        'MaximumRate': 1,
        'CanGoNext': True,
        'CanGoPrevious': True,
        'CanPlay': True,
        'CanPause': True,
        'CanSeek': True,
        'CanControl': True
    }
    spec_props_changed = {
        'PlaybackStatus': 'Paused',
        'LoopStatus': 'Playlist',
        'Rate': 1,
        'Shuffle': True,
        'Metadata': {"mpris:trackid": "/org/mpris/MediaPlayer2/Track/3",
                     "xesam:url": "jazzradio://blues"},
        'Volume': 0.70,
        'CanGoNext': False
    }

    CLS_VIEW = 'Player'
    PATH = 'Player'


class TrackListTestCase(TestCase, BaseTestCase):

    spec_props = {
        'Tracks': ["/org/videolan/vlc/playlist/5"],
        'CanEditTracks': True
    }
    spec_props_changed = {
        'Tracks': ["/org/videolan/vlc/playlist/7"],
        'CanEditTracks': False
    }

    CLS_VIEW = 'TrackList'
    PATH = 'TrackList'


class PlaylistsTestCase(TestCase, BaseTestCase):

    spec_props = {
        "PlaylistCount": 7,
        "Orderings": ["User"],
        "ActivePlaylist": ["/org/mpris/MediaPlayer2/Playlists/12",
                           "jazzradio",
                           ""]
    }
    spec_props_changed = {
        "PlaylistCount": 9,
        "Orderings": ["Alphabetical"],
        "ActivePlaylist": ["/org/mpris/MediaPlayer2/Playlists/10",
                           "newradio",
                           ""]
    }

    CLS_VIEW = 'Playlists'
    PATH = 'Playlists'
