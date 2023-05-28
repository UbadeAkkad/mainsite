from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    
    def items(self):
        return ['home',
                "todo",
                "notes",
                "quiz_list",
                "swagger-ui",
                "leaveamessage",
                "githubaccount",
                "linkedinaccount",]
    
    def location(self, item):
        return reverse(item)
    
    def priority(self, item):
        return {'home': 1.0,
                'todo': 0.7,
                'notes': 0.7,
                "quiz_list": 0.7,
                'swagger-ui': 1.0,
                'leaveamessage': 0.7,
                'githubaccount': 1.0,
                'linkedinaccount': 1.0,}[item]