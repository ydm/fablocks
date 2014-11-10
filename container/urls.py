from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    '',

    url(r'^$', 'container.views.home', name='home'),
    url(r'^fablocks/', include('fablocks.urls', namespace='fablocks')),

    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
