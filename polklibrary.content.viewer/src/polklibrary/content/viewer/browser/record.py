from plone import api
from plone.memoize import ram
from Products.Five import BrowserView
from zope.interface import alsoProvides
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.protect.interfaces import IDisableCSRFProtection

from polklibrary.content.viewer.browser.collection import RelatedContent
from polklibrary.content.viewer.utility import ResourceEnhancer

import random, datetime, time



class RecordView(BrowserView):

    template = ViewPageTemplateFile("templates/record_view.pt")
    enhanced_data = {}
    
    totals = {}
    
    def __call__(self):
        redirect = self.request.form.get('url', self.portal.absolute_url())
        
        if not self.is_oncampus():
            if api.user.is_anonymous():
                return self.request.response.redirect('http://www.uwosh.edu/streaming-videos/login?came_from=' + redirect)
            return self.request.response.redirect('http://www.remote.uwosh.edu/login?url=' + redirect)
            #return self.request.response.redirect('http://www.uwosh.edu/streaming-videos/login?came_from=' + redirect)
            
        alsoProvides(self.request, IDisableCSRFProtection)
        
        like = self.request.form.get('like', None)
        if like:
            self.context.likes += 1 
            
        self.context.visits += 1 
        self.context.reindexObject()
            
        self.load_facet_totals()
        
            
        self.enhanced_data = ResourceEnhancer(self.context.id,self.context.title)
        return self.template()

        
    def load_facet_totals(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        brains = catalog.searchResults(
            portal_type='polklibrary.content.viewer.models.tag_cache',
            review_state='published'
        )
        
        if brains:
            obj = brains[0].getObject()
            self.totals = obj.cache
        else:
            self.totals = {}
            
        
        
    def get_totals(self, type, name):
        try:
            return self.totals.get(type).get(name, 1)
        except Exception as e:
            return 1
        
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
        subject_headings = list(self.context.subject_heading)
        random.seed(datetime.datetime.today().day)
        random.shuffle(subject_headings)
        subject_heading = '|'.join(subject_headings[:2])
        series_title = '|'.join(self.context.series_title)
        data = {
            'series_title' : series_title,
            'subject_heading' : subject_heading,
        }
        
        suburl = 'subject_heading=' + subject_heading + '&series_title=' + series_title
        related = RelatedContent("Similar Films", data, self.portal.absolute_url(), limit=15, sort_by='random', show_query=False)
        related.items = filter(lambda x: x.getId != self.context.getId(), related.items)
        
        return suburl,related
        
        
        
    @ram.cache(lambda *args: time.time() // (60 * 60 * 24 * 7)) # 1 week
    def Totals(self): 
        data = {
            'series_title' : {},
            'subject_heading' : {},
            'associated_entity' : {},
            'geography' : {},
            'genre' : {},
        }
        
        catalog = api.portal.get_tool(name='portal_catalog')
        
        for key,value in data.items():
            index = catalog._catalog.indexes[key]
            
            for k in index.uniqueValues():
            
                t = index._index.get(k)
                if type(t) is not int:
                    data[key][k] = len(t)
                else:
                    data[key][k] = 1
        
        return data
            
        
    @property
    def portal(self):
        return api.portal.get()
        
        