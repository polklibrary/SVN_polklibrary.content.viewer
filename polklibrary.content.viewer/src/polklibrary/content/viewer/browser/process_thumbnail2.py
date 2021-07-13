from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import alsoProvides
from plone.namedfile import NamedBlobImage
import requests, re, json

from polklibrary.content.viewer.utility import VendorInfo
from bs4 import BeautifulSoup
import logging,re,time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger("Plone")

class ThumbnailProcess2(BrowserView):

    logger_on = False
    GET_WAIT = 15

    def __call__(self):
        output = '\n'
        alsoProvides(self.request, IDisableCSRFProtection)
        catalog = api.portal.get_tool(name='portal_catalog')
        options = Options()
        options.headless = True
        driver = webdriver.Chrome('/home/vagrant/Plone/zinstance/chromedriver', options=options)
                
        with api.env.adopt_roles(roles=['Manager']):
        
            process_index = 1
            process_limit = 3
            brains = catalog.searchResults(portal_type='polklibrary.content.viewer.models.contentrecord', image_url="")
            for brain in brains:
                if process_index > process_limit:
                    break;
                process_index += 1
                    
                if VendorInfo.ALEXANDER_STREET_TARGET in brain.getId:
                    output += self.process_aso(driver, brain)
                if VendorInfo.FILMSONDEMAND_TARGET in brain.getId:
                    output += self.process_fod(driver, brain)
                if VendorInfo.KANOPY_TARGET in brain.getId:
                    output += self.process_kan(driver, brain)
                time.sleep(2)
                
        time.sleep(5)
        driver.quit()
                
        return output
        
        
        
    def process_aso(self, driver, brain):
        output = brain.getURL()
        try:          
            withoutproxy = brain.getRemoteUrl.replace('https://www.remote.uwosh.edu/login?url=', '')
            
            driver.implicitly_wait(self.GET_WAIT) # seconds
            driver.get(withoutproxy)
            player_element = driver.find_element_by_css_selector(".nuvo-player--ready")
            thumbnail_attr = player_element.get_attribute("style")
            thumbnail_url = re.search("(?P<url>https?://[^\\s'\"]+)", thumbnail_attr).group("url")
            
            if thumbnail_url:
                obj = brain.getObject()  
                obj.image_url = thumbnail_url
                obj.reindexObject()
                output += ' Thumbnail saved ' + thumbnail_url
            
                if brain.review_state != 'published' and obj.image_url != None and obj.image_url != '':
                    with api.env.adopt_roles(roles=['Manager']):
                        api.content.transition(obj=obj, transition='publish')
                    output += ' -- Published'
                        
        except Exception as e:
            output += ' Error: ' + str(e)
            
        return output + '\n'
        
    def process_fod(self, driver, brain):
        return brain.getURL() + ' FOD not setup \n'
        
    def process_kan(self, driver, brain):
        return brain.getURL() + ' KAN not setup \n'
          
          
        
        
            # recheck = self.request.form.get('recheck', '0')
            # if recheck == '1':
                # brains = catalog.searchResults(portal_type='polklibrary.content.viewer.models.contentrecord', image_url = '/++resource++polklibrary.content.viewer/missing-thumb.png') # bypass security
            # else:
                # brains = catalog.searchResults(portal_type='polklibrary.content.viewer.models.contentrecord', image_url="")
                # #brains = api.content.find(portal_type='polklibrary.content.viewer.models.contentrecord', image_url="")
                # print("else")
                
            # print("Brains: " + str(len(brains)))
            # if brains:
                # brain = brains[0]
                # obj = brain.getObject()
                # title = obj.Title()
                # obj.image_url = '/++resource++polklibrary.content.viewer/missing-thumb.png'
                
                # thumburl = ''
                # try:
                    # # Get Thumbnail
                    # if obj.image == None:
                        # enchanced_data = ResourceEnhancer(obj.id, obj.title)
                        
                        # print("Get Thumbnail")
                        
                        # # add plugin option?
                        # #req = requests.get(enchanced_data['base_url'], verify=False, timeout=15)
                        # #html = req.text
                        
                        # if enchanced_data['name'] == ALEXANDER_STREET_NAME:
                            # thumburl = self.get_alexander_thumbnail_url(enchanced_data)
                        # elif enchanced_data['name'] == KANOPY_NAME:
                            # thumburl = self.get_kanopy_thumbnail_url(enchanced_data)
                        # elif enchanced_data['name'] == FILMSONDEMAND_NAME:
                            # thumburl = self.get_fod_thumbnail_url(enchanced_data)
                        # elif enchanced_data['name'] == SWANK_NAME:
                            # thumburl = self.get_swank_thumbnail_url(enchanced_data)
                        
                        # print ("target thumburl: " + thumburl)
                        
                        # loginfo += " -- Thumbnail: " + thumburl
                        # #return; # stop execution for testing
                        
                        # if thumburl:
                            # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

                            # reqthumb = requests.get(thumburl, headers=headers, timeout=15, allow_redirects=True)
                            
                            
                            
                            
                            # binary = reqthumb.content
                            # loginfo += " -- BINARY: " + str(len(binary))
                            # if len(binary) > 5000:
                                # obj.image = NamedBlobImage(data=reqthumb.content, filename=u'thumb.jpg')
                                # obj.image_url = '/@@download/image/thumb.jpg'
                            # else:
                                # obj.image_url = '/++resource++polklibrary.content.viewer/missing-thumb.png'
                        # else:
                            # obj.image_url = '/++resource++polklibrary.content.viewer/missing-thumb.png'
                            
                                    
                            
                # except Exception as e:
                    # error_msg = '!! RETRIEVE ERROR: ' + str(e) + ' - ' + brains[0].getPath() + '   URL:' + thumburl
                 
                # try:
                    # if brain.review_state != 'published' and obj.image != None:
                        # with api.env.adopt_roles(roles=['Manager']):
                            # api.content.transition(obj=obj, transition='publish')
                            
                # except Exception as e:
                    # error_msg = '!! PUBLISH ERROR: ' + str(e) + ' - ' + brains[0].getPath()  + '   URL:' + thumburl
                        
                # # Reindex catalog    
                # with api.env.adopt_roles(roles=['Manager']):
                    # obj.reindexObject()
            
            # if self.logger_on:
                # logger.info(loginfo)
                # logger.info(error_msg)
                
        # return 'Processed Thumbnail: ' + title + ' Remaining: ' + str((len(brains)-1)) + '  INFO: ' + error_msg

        
    # def get_kanopy_thumbnail_url(self, enchanced_data):
        # print("KANOPY PROCESS - function last checked 6/21/2021")
        # url = 'https://uwosh.kanopy.com/node/' + enchanced_data['id'] + '/preview'
        # req = requests.get(url, verify=False, timeout=15)
        # html = req.text
        
        # soup = BeautifulSoup(html)
        # element = soup.select_one('span.image.fluid img')
        
        # try:
            # return element.get('src')
        # except Exception as e:
            # print("ERROR: " + str(e))
        # return ''
        
    # def get_fod_thumbnail_url(self, enchanced_data):
        # print("FOD PROCESS - function last checked 6/21/2021")
        # return 'https://fod.infobase.com/image/' + str(enchanced_data['id'])
        
                
    # def get_swank_thumbnail_url(self, enchanced_data):
        # print('SWANK PROCESS')
        
        # return ''

        
        
    # def get_alexander_thumbnail_url(self, enchanced_data):
        # print("ASP PROCESS - function last checked 6/21/2021")
        
        # url = 'https://search.alexanderstreet.com/view/work/bibliographic_entity|video_work|' + enchanced_data['id']
        # req = requests.get(url, verify=False, timeout=15)
        # html = req.text
        
        # soup = BeautifulSoup(html)
        # scripts = soup.findAll(lambda tag: (tag.name == 'script' and len(tag.attrs) == 0) and 'original.jpg' in tag.text)
        # if scripts:
            # try:
                # text = scripts[0].getText().lstrip('jQuery.extend(Drupal.settings,').rstrip(');')
                # data = json.loads(text)
                # return data['ASP']['Lazr']['Uniplayer']['timeline']['chunkData']['infoPanelFullSizeImageUrl']
            # except:
                # pass
        # else:
            # try:
                # scripts = soup.findAll('script', {'type':'application/ld+json'})
                # if scripts:
                    # data = json.loads(scripts[0].getText())
                    # return data['thumbnail']['contentUrl'].replace('fit-140x140.jpg', 'fit-140x140.jpg')
            # except:
                # pass
        # return ''
        
        
    @property
    def portal(self):
        return api.portal.get()
        
        