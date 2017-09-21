from plone import api
from plone.i18n.normalizer import idnormalizer
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility, getMultiAdapter
from zope.container.interfaces import INameChooser
import random, time, transaction

from polklibrary.content.viewer.browser.collection import AdvancedCollectionQuery



class GroupList(BrowserView):

    template = ViewPageTemplateFile("templates/group_list.pt")
    
    def __call__(self):
        return self.template()

    # Cache later?
    def get_collections(self):
    
        catalog = api.portal.get_tool(name='portal_catalog')
        brains = catalog.searchResults(
            portal_type='polklibrary.content.viewer.models.collection',
            review_state='published',
            id={
                "query": self.context.collections,
                "operator" : 'or',
            },
        )
        
        collections = []
        for brain in brains:
            collections.append(AdvancedCollectionQuery(brain, limit=15, start=0, sort_by=brain.sort_type, sort_direction=brain.sort_direction))
    
        return collections
        
        
    @property
    def portal(self):
        return api.portal.get()
        
        