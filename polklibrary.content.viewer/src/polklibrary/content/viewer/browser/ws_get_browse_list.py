from plone import api
from plone.memoize import ram
from Products.Five import BrowserView

import json

class WSView(BrowserView):

    _data = {}
    
    #@ram.cache(lambda *args: time() // (60 * 10))
    def __call__(self):
        self._data = []
        self.process()
        
        if self.request.form.get('alt','') == 'jsonp':
            return self.request.form.get('callback','?') + '(' + json.dumps(self._data) + ')'
        return json.dumps(self._data)

        
    def process(self):
        brains = api.content.find(portal_type='polklibrary.content.viewer.models.collection', 
                                     sort_on="sortable_title", 
                                     enabled_browse=True)
        for brain in brains:
            self._data.append({
                'Title': brain.Title,
                'Description': brain.Description,
                'getURL': brain.getURL(),
            })
        

    @property
    def portal(self):
        return api.portal.get()
        