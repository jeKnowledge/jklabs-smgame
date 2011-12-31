from django.conf.urls.defaults import patterns, include, url

from gamepress.views import bloglist, article_view
from gamecore.views import trading, proposal_view, buy, wallet, addproposal, eventdetails, companypage
from playerinfo.views import home , dashboard, exit_game, profile, send
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
    url(r'^addproposal/(?P<invest_id>\d+)/$', addproposal, name='addproposal'),
    url(r'^press/$', bloglist, name='bloglist'),
    url(r'^press/(?P<art_id>\d+)/$', article_view, name='article_view'),
    url(r'^profile/(?P<user_id>\d+)/$', profile, name='profile'),
    url(r'^event/(?P<event_id>\d+)/$', eventdetails, name='eventdetails'),
    url(r'^msgsend/$', send, name='send'),
    url(r'^company/(?P<company_id>\d+)/$', companypage, name='companypage'),
)
