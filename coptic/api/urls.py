from django.conf.urls import url
from api import views

app_name = 'api'

urlpatterns = [
    url(r'^corpora/$', views.api, {'params': 'corpora'}, name='corpus-list'),
    url(r'^corpora/(?P<corpus_slug>[\w-]+)/texts/$', 
        views.api, {'params': 'texts'}, name='text-list'),
    url(r'^corpora/(?P<corpus_slug>[\w-]+)/texts/(?P<text_slug>[\w-]+)/$', 
        views.api, {'params': 'text-detail'}, name='text-detail'),
    url(r'^corpora/(?P<corpus_slug>[\w-]+)/texts/(?P<text_slug>[\w-]+)/(?P<format_slug>[\w-]+)/$',
        views.api, {'params': 'visualization'}, name='visualization'),
    # Catch-all for backward compatibility
    url(r'^(?P<params>.*)$', views.api, name='api'),
]