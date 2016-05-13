from django.conf.urls import patterns, include, url
from django.contrib import admin

#from OctoProject.login import views
#from django.contrib.auth.urls
urlpatterns = patterns('',
    # Examples:
 #    url(r'^$', 'OctoProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
#   url('^',include('django.contrib.auth.urls'))
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','login.views.index'),
    url(r'^signin/','login.views.signin'),
    url(r'^signout/','login.views.signout' ),
    url(r'^table/$','login.views.table' ),
    url(r'^test/$','login.views.test' ),
    url(r'^test2/$','login.views.test2' ),
    url(r'^tabletest/$','login.views.tabletest' ),
    url(r'^search/edit/(?P<tag>.+)','login.views.search' ),
    url(r'^search/$','login.views.search' ),
    url(r'^search/[0-9A-Za-z_\-]+/$','login.views.search' ),
    url(r'^NewStream/$','login.views.NewStream' ),
    url(r'^allstream/$','login.views.allstream' ),
    url(r'^Holger/$','login.views.Holgerstreams' ),
    url(r'^Holger/edit/(?P<tag>.+)','login.views.Holgerstreams' ),
    url(r'^lstream/$','login.views.listtream' ),
    url(r'^lstream/(?P<tag>.+)','login.views.listtream' ),
    url(r'^delstream/(?P<tagasp>.+)/(?P<tag>.+)','login.views.deletestream' ),
    url(r'^deletestreamconfirm/$','login.views.deletestreamconfirm' ),
    url(r'^dbview/$','login.views.dbview'),
    url(r'^NewCust/$','login.views.NewCust'),
    url(r'^EditStream/$','login.views.EditStream'),
    url(r'^Editabr/(?P<tag>.+)','login.views.Editabr' ),
    url(r'^Updateabr/$','login.views.Updateabr' ),
    url(r'^advconfig/(?P<tag>.+)$','login.views.advconfig' ),
    #url(r'^(?P<slug>[-\w]+)/$', login.views.search.as_view(), name='article-detail'),
    
    url(
        r'^login/$',
        'django.contrib.auth.views.login',
        name='login',
        kwargs={'template_name': 'account:login.html'}
    ),
       
    url(r'^accounts/password_reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'), 
    url(r'^accounts/password_reset/complete/$' , 
        'django.contrib.auth.views.password_reset_complete',
        name='password_reset_complete'),                
    # Password Reset URLs:

    
    url(r'^accounts/password_reset/$', 
        'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/accounts/password_reset/mailed/'},
        name="password_reset"),
    (r'^accounts/password_reset/mailed/$',
        'django.contrib.auth.views.password_reset_done'),
    (r'^accounts/password_reset/(?P<uidb64>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect' : '/accounts/password_reset/complete/'}),
    
                       
)
