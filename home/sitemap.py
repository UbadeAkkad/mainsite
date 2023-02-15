from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    
    def items(self):
        return ['home',"githubaccount","leaveamessage","swagger-ui",]
    
    def location(self, item):
        return reverse(item)
    
    def priority(self, item):
        return {'home': 1.0, 'githubaccount': 1.0, 'leaveamessage': 0.7, 'swagger-ui': 0.6}[item]