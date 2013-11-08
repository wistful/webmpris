from django.conf.urls import patterns, url
from webmpris.views import Root, Player, TrackList, Playlists

OBJ_MAP = {'Root': Root,
           'Player': Player,
           'TrackList': TrackList,
           'Playlists': Playlists}


urlpatterns = patterns(
    'webmpris.views',
    url(r'^players$', 'get_players', name='players'),
)

for name, obj in OBJ_MAP.items():
    url_prop = r'^players/(?P<player_id>:[\w.]+)/{name}$'.format(name=name)
    url_meth = url_prop[:-1] + r'/(?P<method_name>[\w]+$)'
    urlpatterns += patterns(
        '',
        url(url_prop, obj.as_view()),
        url(url_meth, obj.as_view()),
    )
