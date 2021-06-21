from plone import api
from plone.i18n.normalizer import idnormalizer
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility, getMultiAdapter
from zope.container.interfaces import INameChooser
from AccessControl import getSecurityManager
from AccessControl import Unauthorized
from Products.CMFCore.permissions import ModifyPortalContent

import random, time, re

from polklibrary.content.viewer.utility import BrainsToCSV
from polklibrary.content.viewer.browser.collection import CollectionObject
from polklibrary.content.viewer.utility import ResourceEnhancer


class Search(BrowserView):

    template = ViewPageTemplateFile("templates/search.pt")
    
    def __call__(self):        
        if self.request.form.get('form.csv.submit', None) or self.request.form.get('csv', None):
            self.request.response.setHeader("Content-Disposition", "attachment;filename=collection.csv")
            return BrainsToCSV(self.get_collection().items)
            
        return self.template()
    
        
    def get_collection(self):
        queryraw = self.request.form.get('form.query','').lower().strip()
        start = int(self.request.form.get("start", 0))
        limit = int(self.request.form.get("limit", 50))
        sort_on = self.request.form.get('form.sort','sortable_title')
        sort_order = self.request.form.get('form.sort.direction','ascending')
        
        if queryraw and queryraw != '*':
            query = queryraw.replace(' and ', ',').replace(' or ', ',').replace(';', ',')
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
            
            query_values = '?form.sort=' + sort_on + '&form.sort.direction=' + sort_order + '&form.query=' + queryraw
            return CollectionObject("Results Found", self.portal.absolute_url() + '/find' + query_values , brains[start:start+limit], len(brains), start, limit)
        
        elif queryraw == '*':
            query = queryraw.replace(' and ', ',').replace(' or ', ',').replace(';', ',')
            query = query.split(',')
            
            catalog = api.portal.get_tool(name='portal_catalog')
            
            sm = getSecurityManager()
            if sm.checkPermission(ModifyPortalContent, self.context):
                brains = catalog.searchResults(
                    portal_type='polklibrary.content.viewer.models.contentrecord',
                    sort_on=sort_on, 
                    sort_order=sort_order
                )
            else:
                brains = catalog.searchResults(
                    portal_type='polklibrary.content.viewer.models.contentrecord',
                    review_state='published',
                    sort_on=sort_on, 
                    sort_order=sort_order
                )
            
            query_values = '?form.sort=' + sort_on + '&form.sort.direction=' + sort_order + '&form.query=' + queryraw
            return CollectionObject("Results Found", self.portal.absolute_url() + '/find' + query_values , brains[start:start+limit], len(brains), start, limit)
        
        return CollectionObject("Results Found", self.portal.absolute_url() + '/find', [], 0, start, limit)
        
    @property
    def portal(self):
        return api.portal.get()
        
        
        