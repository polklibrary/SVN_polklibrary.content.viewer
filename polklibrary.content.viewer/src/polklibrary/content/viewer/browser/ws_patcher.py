from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides
from plone.i18n.normalizer import idnormalizer
from plone.memoize import ram
from Products.Five import BrowserView

import json, transaction

class WSView(BrowserView):

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
    
        found = 0
        brains = api.content.find(portal_type='polklibrary.content.viewer.models.contentrecord')
        for brain in brains:
            if 'aspasp' in brain.getId:
                newid = brain.getId.replace('aspasp','asp')
                api.content.rename(obj=brain.getObject(), new_id=newid)
                found+=1
            elif 'kankan' in brain.getId:
                newid = brain.getId.replace('kankan','kan')
                api.content.rename(obj=brain.getObject(), new_id=newid)
                found+=1
            elif 'fodfod' in brain.getId:
                newid = brain.getId.replace('fodfod','fod')
                api.content.rename(obj=brain.getObject(), new_id=newid)
                found+=1
    
        return 'Done: ' + str(found)
            

    @property
    def portal(self):
        return api.portal.get()
        