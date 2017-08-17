from plone import api
from Products.Five import BrowserView
from zope.interface import alsoProvides
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.protect.interfaces import IDisableCSRFProtection

from polklibrary.content.viewer.browser.collection import RelatedContent
from polklibrary.content.viewer.utility import ResourceEnhancer

import random, datetime

class RecordView(BrowserView):

    template = ViewPageTemplateFile("templates/record_view.pt")
    enhanced_data = {}
    
    def __call__(self):
        redirect = self.request.form.get('url', self.portal.absolute_url())
        if not self.is_oncampus():
            return self.request.response.redirect('http://www.remote.uwosh.edu/login?url=' + redirect)
        
        alsoProvides(self.request, IDisableCSRFProtection)
        
        like = self.request.form.get('like', None)
        if like:
            self.context.likes += 1 
            
        self.context.visits += 1 
        self.context.reindexObject()
            
        self.enhanced_data = ResourceEnhancer(self.context.id,self.context.title)
        return self.template()

        
    def is_oncampus(self):
        dev_restriction = '10.0.2.2'
        ip_restriction = '141.233.'
        ip = ''
        if 'HTTP_X_FORWARDED_FOR' in self.request.environ:
            ip = self.request.environ['HTTP_X_FORWARDED_FOR'] # Virtual host
        elif 'HTTP_HOST' in self.request.environ:
            ip = self.request.environ['REMOTE_ADDR'] # Non-virtualhost
        ipl = ip.split(',')
        
        return ipl[0].strip().startswith(ip_restriction) or ipl[0].strip().startswith(dev_restriction)
        
    def get_related(self):
        type = 'subject_heading'
        query_list = list(self.context.subject_heading)
        random.seed(datetime.datetime.today().day)
        random.shuffle(query_list)
        query = ','.join(query_list[:2])
        return type,query,RelatedContent("Similar Films", type, query, self.portal.absolute_url(), limit=15, sort_by='random', show_query=False)
        
        
    @property
    def portal(self):
        return api.portal.get()
        
        