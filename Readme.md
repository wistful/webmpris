# webmpris #
This is a Python wrapper around the MPRIS2 interfaces of media players.

## Requires ##

[pympris>=1.0](https://github.com/wistful/pympris).

## License ##
See the `LICENSE` file.

## Setup ##

Either clone this repository into your project, or install with `pip install webmpris`

You'll need to add `webmpris` to `INSTALLED_APPS` in you projects settings.py file:

```python
INSTALLED_APPS = (
    ...
    'webmpris',
)
```

## Supported MPRIS Interfaces ##

`webmpris` supports all MPRIS2 D-Bus Intefaces:

-  [org.mpris.MediaPlayer2](http://specifications.freedesktop.org/mpris-spec/latest/Media_Player.html)
-  [org.mpris.MediaPlayer2.Player](http://specifications.freedesktop.org/mpris-spec/latest/Player_Interface.html)
-  [org.mpris.MediaPlayer2.TrackList](http://specifications.freedesktop.org/mpris-spec/latest/Track_List_Interface.html)
-  [org.mpris.MediaPlayer2.Playlists](http://specifications.freedesktop.org/mpris-spec/latest/Playlists_Interface.html)

**Note**:  The media player must implement the following interfaces:

-  org.mpris.MediaPlayer2
-  org.mpris.MediaPlayer2.Player

The media player **may** implement the org.mpris.MediaPlayer2.TrackList interface.

The media player **may** implement the org.mpris.MediaPlayer2.Playlists interface.


## REST API ##

Default content type : `application/json`

Requests:

-     `GET` uses to return players ids, or players properties.
-     `PUT` uses to change players properties.
-     `POST` uses to do some actions with player
    arguments sends as a `{'args': [arg1, arg2, ...]}`` json object.

URLs formats:

- `/players/[id]/[iface]` (use `GET` and `PUT` requests)
- `/players/[id]/[iface]/[method]` (use `POST` requests)

where:

`[iface]` describes mpris interface: `Root`, `Player`, `TrackList`, `Playlists`  
`[method]` describes interfaces method.  

### /players ###
`GET /players` returns list of available players ids.

### /players/[id]/Root ###
implements [org.mpris.MediaPlayer2](http://specifications.freedesktop.org/mpris-spec/latest/Media_Player.html)  

`GET /players/[id]` returns properties.

`PUT /players[id]` changes properties.

### /players/[id]/Root/[method] ###

`POST /players[id]/Root/Raise` brings the media player's user interface to the front using any appropriate mechanism available. 

`POST /players[id]/Root/Quit` causes the media player to stop running.

### /players/[id]/Player ###
implements [ org.mpris.MediaPlayer2.Player ](http://specifications.freedesktop.org/mpris-spec/latest/Player_Interface.html)  

`GET /players/[id]/Player` returns properties

`PUT /players/[id]/Player` changes properties

### /players/[id]/Player/[method] ###
available methods:

- `Next`, arguments are not required
- `Previous`, arguments are not required
- `Pause`, arguments are not required
- `PlayPause`, arguments are not required
- `Stop`, arguments are not required
- `Play`, arguments are not required
- `Seek`, arguments: int *offset* 
- `SetPosition`, arguments: str *TrackID*, int *Position*
- `OpenUri`, arguments: str *Uri*

### /players/[id]/TrackList ###
implements [org.mpris.MediaPlayer2.TrackList](http://specifications.freedesktop.org/mpris-spec/latest/Track_List_Interface.html)  

`GET /players/[id]/TrackList` returns properties

`PUT /players/[id]/TrackList` changes properties

### /players/[id]/TrackList/[method] ###
available methods:

- `GetTracksMetadata`, arguments: [str *TrackIds*]
- `AddTrack`, arguments: str *Uri*, str *AfterTrack*, bool *SetAsCurrent*
- `RemoveTrack`, arguments: str *TrackId*
- `GoTo`, arguments: str *TrackId*

### /players/[id]/Playlists ###
implements [org.mpris.MediaPlayer2.Playlists](http://specifications.freedesktop.org/mpris-spec/latest/Playlists_Interface.html)

`GET /players/[id]/Playlists` returns properties

`PUT /players/[id]/Playlists` changes properties

### /players/[id]/Playlists/[method] ###
available methods:

- `ActivatePlaylist`, arguments: str *PlaylistId*
- `GetPlaylists`, arguments: int *Index*, int *MaxCount*, str *Order*, bool *ReverseOrder*


## Examples ##

### Get available players ###
Request: `curl -i -H "Accept: application/json" -X GET "http://127.0.0.1:8000/webmpris/players"`

Response:
```json
[":1.10336", ":1.9878", ":1.9904"]
```

### org.mpris.MediaPlayer2 interface ###

**Properties**

Request: `curl -i -H "Accept: application/json" -X GET "http://127.0.0.1:8000/webmpris/players/:1.9904/Root"`

Response: ```JSON
{"Fullscreen": false, "HasTrackList": true, "CanSetFullscreen": false, "SupportedUriSchemes": ["file", "http", "cdda", "smb", "sftp"], "CanQuit": true, "DesktopEntry": "clementine", "CanRaise": true, "SupportedMimeTypes": ["application/ogg", "application/x-ogg", "application/x-ogm-audio", "audio/aac", "audio/mp4", "audio/mpeg", "audio/mpegurl", "audio/ogg", "audio/vnd.rn-realaudio", "audio/vorbis", "audio/x-flac", "audio/x-mp3", "audio/x-mpeg", "audio/x-mpegurl", "audio/x-ms-wma", "audio/x-musepack", "audio/x-oggflac", "audio/x-pn-realaudio", "audio/x-scpls", "audio/x-speex", "audio/x-vorbis", "audio/x-vorbis+ogg", "audio/x-wav", "video/x-ms-asf", "x-content/audio-player"], "Identity": "Clementine"}
```

Request: ` curl -i -H "Accept: application/json" -X PUT -d "{\"Fullscreen\": true}" "http://127.0.0.1:8000/webmpris/players/:1.9904/Root"`

Response: `{"errmsg": []}`

**Methods**

Request: `curl -i -H "Accept: application/json" -X POST "http://127.0.0.1:8000/webmpris/players/:1.9904/Root/Raise"`

Response: `{"status": "success", "result": null}`

### org.mpris.MediaPlayer2.Player interface ###

**Properties**
Request: ` curl -i -H "Accept: application/json" -X GET "http://127.0.0.1:8000/webmpris/players/:1.9904/Player"`

Response: ```JSON
{"CanGoNext": true, "Shuffle": false, "CanControl": true, "LoopStatus": "Track", "CanPause": true, "PlaybackStatus": "Paused", "Volume": 0.5, "Rate": 1.0, "CanPlay": true, "CanSeek": false, "Position": 758503033, "CanGoPrevious": true, "MaximumRate": dbus.Double(1.0, variant_level=1), "Metadata": {"mpris:trackid": "/org/mpris/MediaPlayer2/Track/1", "xesam:artist": ["Billy Eckstine"], "mpris:artUrl": "file:///tmp/clementine-art-E19378.jpg", "xesam:url": "jazzradio://vocallegends", "xesam:title": "Ill Wind"}}
```

Request: `curl -i -H "Accept: application/json" -X PUT -d "{\"Volume\": 0.7}" "http://127.0.0.1:8000/webmpris/players/:1.9904/Player"`

Response: `{"errmsg": []}`

**Methods**

Use `PlayPause` method:

Request: `curl -i -H "Accept: application/json" -X POST "http://127.0.0.1:8000/webmpris/players/:1.9904/Player/PlayPause"`

Response: `{"status": "success", "result": null}`

Use method with argument:

Request with arguments: `curl -i -H "Accept: application/json" -X POST -d "{\"args\": [-50000]}" "http://127.0.0.1:8000/webmpris/players/:1.9904/Player/Seek"`

Respnonse: `{"status": "success", "result": null}`


Use method with two arguments:

Request: `curl -i -H "Accept: application/json" -X POST -d "{\"args\": [\"/org/mpris/MediaPlayer2/Track/2\", 1250000]}" "http://127.0.0.1:8000/webmpris/players/:1.9904/Player/SetPosition"`

Respnonse: `{"status": "success", "result": null}`