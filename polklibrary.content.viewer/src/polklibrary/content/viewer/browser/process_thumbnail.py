from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import alsoProvides
from plone.namedfile import NamedBlobImage
import requests, re, json

from polklibrary.content.viewer.utility import ResourceEnhancer, ALEXANDER_STREET_NAME, KANOPY_NAME, FILMSONDEMAND_NAME
from BeautifulSoup import BeautifulSoup
import logging,transaction

logger = logging.getLogger("Plone")

class ThumbnailProcess(BrowserView):

    
    
    def __call__(self):
        loginfo = ''
        alsoProvides(self.request, IDisableCSRFProtection)
        title = 'No results'
        error_msg = ''    
        catalog = api.portal.get_tool(name='portal_catalog')
        
        recheck = self.request.form.get('recheck', '0')
        if recheck == '1':
            brains = catalog.unrestrictedSearchResults(portal_type='polklibrary.content.viewer.models.contentrecord', image_url = '/++resource++polklibrary.content.viewer/missing-thumb.png') # bypass security
        else:
            brains = catalog.unrestrictedSearchResults(portal_type='polklibrary.content.viewer.models.contentrecord', image_url=None)

        if brains:
            brain = brains[0]
            with api.env.adopt_roles(roles=['Manager']):
                obj = brain.getObject()
            title = obj.Title()
            
            try:
                # Get Thumbnail
                if obj.image == None:
                    enchanced_data = ResourceEnhancer(obj.id,obj.title)
                    
                    # add plugin option?
                    req = requests.get(enchanced_data['base_url'], verify=False)
                    html = req.text
                    
                    thumburl = ''
                    if enchanced_data['name'] == ALEXANDER_STREET_NAME:
                        thumburl = self.get_alexander_thumbnail_url(html)
                    elif enchanced_data['name'] == KANOPY_NAME:
                        thumburl = self.get_kanopy_thumbnail_url(html)
                    elif enchanced_data['name'] == FILMSONDEMAND_NAME:
                        thumburl = self.get_fod_thumbnail_url(html)
                        
                    loginfo += " -- Thumbnail: " + thumburl
                    #return; # stop execution for testing
                    
                    if thumburl:
                        reqthumb = requests.get(thumburl, verify=False)
                        binary = reqthumb.content
                        loginfo += " -- BINARY: " + str(len(binary))
                        if len(binary) > 5000:
                            obj.image = NamedBlobImage(data=reqthumb.content, filename=u'thumb.jpg')
                            obj.image_url = '/@@download/image/thumb.jpg'
                        else:
                            obj.image_url = '/++resource++polklibrary.content.viewer/missing-thumb.png'
                    else:
                        obj.image_url = '/++resource++polklibrary.content.viewer/missing-thumb.png'
                        
                                
                        
            except Exception as e:
                error_msg = '!! ERROR: ' + str(e) + ' - ' + brains[0].getPath()
             
            try:
                if brain.review_state != 'published' and obj.image != None:
                    with api.env.adopt_roles(roles=['Manager']):
                        api.content.transition(obj=obj, transition='publish')
                        
            except Exception as e:
                error_msg = '!! ERROR: ' + str(e) + ' - ' + brains[0].getPath()
                    
            # Reindex catalog    
            #obj.reindexObject(idxs=["image_url"])
            
            with api.env.adopt_roles(roles=['Manager']):
                obj.reindexObject()
            #catalog.reindexObject(obj)
                
                
        logger.info(loginfo)
        return 'Processed Thumbnail: ' + title + ' Remaining: ' + str((len(brains)-1)) + '  INFO: ' + error_msg

        
    def get_kanopy_thumbnail_url(self, html):
        print "KANOPY PROCESS"
        soup = BeautifulSoup(html)
        img = soup.findAll(lambda tag: (tag.name == 'div' and  tag.has_key('data-thumbnail')))
        print len(img)
        
        if img:
            try:
                return 'https://uwosh.kanopystreaming.com' + img[0].get('data-thumbnail')
            except Exception as e:
                print "ERROR: " + str(e)
        return ''
        
    def get_fod_thumbnail_url(self, html):
        print "FOD PROCESS"
        soup = BeautifulSoup(html)
        img = soup.findAll(attrs={'id' : 'ctl00_MainContent_fpImg'})
        if img:
            try:
                return img[0].get('src').replace('width/252','width/400')
            except Exception as e:
                print "ERROR: " + str(e)
        return ''
        
        
    def get_alexander_thumbnail_url(self, html):
        print "ALEX PROCESS"
        soup = BeautifulSoup(html)
        
        scripts = soup.findAll(lambda tag: (tag.name == 'script' and len(tag.attrs) == 0) and 'original.jpg' in tag.text)
        if scripts:
            try:
                text = scripts[0].getText().lstrip('jQuery.extend(Drupal.settings,').rstrip(');')
                data = json.loads(text)
                return data['ASP']['Lazr']['Uniplayer']['timeline']['chunkData']['infoPanelFullSizeImageUrl']
            except:
                pass
        else:
            try:
                scripts = soup.findAll('script', {'type':'application/ld+json'})
                if scripts:
                    data = json.loads(scripts[0].getText())
                    return data['thumbnail']['contentUrl'].replace('fit-140x140.jpg', 'fit-140x140.jpg')
            except:
                pass
        return ''
        
        
        
    @property
    def portal(self):
        return api.portal.get()
        
        