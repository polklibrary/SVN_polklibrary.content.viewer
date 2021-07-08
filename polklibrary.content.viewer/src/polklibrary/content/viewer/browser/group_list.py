from plone import api
from plone.i18n.normalizer import idnormalizer
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility, getMultiAdapter
from zope.container.interfaces import INameChooser
from polklibrary.content.viewer.utility import CleanID
import random, time, transaction

from polklibrary.content.viewer.browser.collection import AdvancedCollectionQuery



class GroupList(BrowserView):

    template = ViewPageTemplateFile("templates/group_list.pt")
    
    def __call__(self):
        return self.template()

    # Cache later?
    def get_collections(self):
    
        catalog = api.portal.get_tool(name='portal_catalog')
        ordered_brains = []
        for collection in self.context.collections:
            brains = catalog.searchResults(
                portal_type='polklibrary.content.viewer.models.collection',
                review_state='published',
                id=collection,
            )
            if brains:
                ordered_brains.append(brains[0])
        
        collections = []
        for brain in ordered_brains:
            collections.append(AdvancedCollectionQuery(brain, limit=15, start=0, sort_by=brain.sort_type, sort_direction=brain.sort_direction))
    
        return collections
        
    def get_direct_image(self, item):
        if item.id.startswith('fod'):
            id = CleanID(item.id)
            return 'https://fod.infobase.com/image/' + str(id)
        if item.image_url == '' or '++resource++' in item.image_url:
            return '++resource++polklibrary.content.viewer/missing-thumb.png'
        return item.getURL() + item.image_url
        
    @property
    def portal(self):
        return api.portal.get()
        
        