__version__ = '1.0'
__description__ = 'REST API to control media players via MPRIS2 interfaces'
requires = [
    'pympris'
]

README = """webmpris is a REST API
to control media players via MPRIS2 interfaces.

Supported intefaces:
org.mpris.MediaPlayer2              via /players/<id>/Root
org.mpris.MediaPlayer2.Player       via /players/<id>/Player
org.mpris.MediaPlayer2.TrackList    via /players/<id>/TrackList
org.mpris.MediaPlayer2.Playlists    via /players/<id>/Playlists

"""
