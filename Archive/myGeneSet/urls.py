from django.conf.urls import patterns, include, url
from vbitext.views import analyze, query, display_meta, create_file, disp_abs, robots
from vbitext.views import reanalyze, more_abs, visualize, about
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^query', query),
	 url(r'^analyze', analyze),
	 url(r'^meta', display_meta),
     url(r'^abs', disp_abs),
	 url(r'^reanalyze', reanalyze),
	 url(r'^more_abs', more_abs),
	 url(r'^$',query),
	 url(r'^visualize',visualize),
	 url(r'robots.txt', robots),
	 url(r'about', about),
	 
	 url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # Uncomment the admin/doc line below to enable admin documentation:
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
)
