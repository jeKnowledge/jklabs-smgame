from django.conf.urls.defaults import patterns, include, url

from gamecore.views import trading, proposal_view, buy, wallet
from playerinfo.views import home , dashboard, exit_game
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'', include('social_auth.urls')),
    # Examples:
    # url(r'^$', 'stock_market_game.views.home', name='home'),
    # url(r'^stock_market_game/', include('stock_market_game.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^trading/$', trading , name='trading'),
    url(r'^trading/(?P<prop_id>\d+)/$', proposal_view, name='proposal_view'),
    url(r'^$', home, name='home'),
    url(r'^logout/$', exit_game, name='exit_game'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^buy/(?P<prop_id>\d+)/$', buy, name='buy'),
    url(r'^wallet/$', wallet, name='wallet'),
)
