from plone import api
from plone.i18n.normalizer import idnormalizer
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility, getMultiAdapter
from zope.container.interfaces import INameChooser
import random, time, re

from polklibrary.content.viewer.browser.collection import CollectionObject
from polklibrary.content.viewer.utility import ResourceEnhancer

class Search(BrowserView):

    template = ViewPageTemplateFile("templates/search.pt")
    
    def __call__(self):
        return self.template()
    
        
    def get_collection(self):
        sort_on = self.request.form.get('form.sort','sortable_title')
        sort_order = self.request.form.get('form.sort.direction','ascending')
        
        query = self.request.form.get('form.query','').lower()
        if query:
            query = query.replace(' and ', ',').replace(' or ', ',').replace(';', ',')
            query = query.split(',')
            
            catalog = api.portal.get_tool(name='portal_catalog')
            brains = catalog.searchResults(
                portal_type='polklibrary.content.viewer.models.contentrecord',
                review_state='published',
                SearchableText={
                    "query": query,
                    "operator" : 'or',
                },
                sort_on=sort_on, 
                sort_order=sort_order
            )
            
            return CollectionObject("Results", self.portal.absolute_url() + '/find', brains)
        return CollectionObject("Results", self.portal.absolute_url() + '/find', [])
        
    @property
    def portal(self):
        return api.portal.get()
        
        
        