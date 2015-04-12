from django import http
#from django.contrib.sites.shortcuts import *
from django.conf import settings
from django.contrib.sites.models import Site
from urlparse import urlparse

 
class MultiSiteMiddleware(object):
    def process_request(self, request):
        host = request.META['HTTP_HOST']
        site = Site.objects.get(domain=host)
        settings.SITE_ID = site.id
        
        Site.objects.clear_cache()
        return
       
