from plone import api
from plone.i18n.normalizer import idnormalizer
from plone.memoize import ram
from Products.Five import BrowserView

import json, transaction

class WSView(BrowserView):

    _data = {}
    
    def __call__(self):
        self._data = {
            'status' : 200
        }
        if not api.user.is_anonymous():
            self.process()
        else:
            self._data['status'] = 403
        
        if self.request.form.get('alt','') == 'jsonp':
            return self.request.form.get('callback','?') + '(' + json.dumps(self._data) + ')'
        return json.dumps(self._data)

    def process(self):
        user = api.user.get_current()
        id = self.request.form.get('id','')
        type = self.request.form.get('type','')
        films = user.saved_films
                
        try:
            if user:
                id = idnormalizer.normalize(id) + '|'
                if type == 'add' and id:
                    user.saved_films += id
                    transaction.commit()
                elif type == 'remove' and id:
                    user.saved_films = user.saved_films.replace(id, '')
                    transaction.commit()
        except:
            self._data['status'] = 400
            
        self._data['data'] = user.saved_films

    @property
    def portal(self):
        return api.portal.get()
        