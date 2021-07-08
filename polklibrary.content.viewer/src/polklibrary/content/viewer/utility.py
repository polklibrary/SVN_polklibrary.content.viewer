from plone import api
from plone.memoize import ram
from plone.i18n.normalizer import idnormalizer
from unidecode import unidecode
import re, time, ftfy, csv, io

# used elsewhere to target
ALEXANDER_STREET_NAME = 'Alexander Street'
KANOPY_NAME = 'Kanopy'
FILMSONDEMAND_NAME = 'Films on Demand'
SWANK_NAME = 'Swank'
ALMA_NAME = 'Catalog'
OTHER_NAME = 'Other'

ALEXANDER_STREET_TARGET = 'asp'
KANOPY_TARGET = 'kan'
FILMSONDEMAND_TARGET = 'fod'
SWANK_TARGET = 'swa'
ALMA_TARGET = 'uwi'



class Tools(object):



    def get_image_by_obj(self, o=None):
        if not o:
            o = self.context
        if o.image_url:
            if '@@images' in o.image_url:
                return o.absolute_url() + o.image_url
            return o.image_url
        return o.absolute_url() + '/++resource++polklibrary.content.viewer/missing-thumb.png'
        
    def get_image_by_brain(self, o):
        if o.image_url:
            if '@@images' in o.image_url:
                return o.getURL() + o.image_url
            return o.image_url
        return o.getURL() + '/++resource++polklibrary.content.viewer/missing-thumb.png'
        
    def get_vender_name(self, o=None):
        if not o:
            o = self.context
        if ALEXANDER_STREET_TARGET in o.id.lower():   
            return ALEXANDER_STREET_NAME
        elif FILMSONDEMAND_TARGET in o.id.lower():   
            return FILMSONDEMAND_NAME
        elif KANOPY_TARGET in o.id.lower():   
            return KANOPY_NAME
        elif SWANK_TARGET in o.id.lower():   
            return SWANK_NAME
        elif ALMA_TARGET in o.id.lower():   
            return ALMA_NAME
        else:
            return OTHER_NAME
        
    # try:
        # obj = o.getObject()
    # except:
        # pass
    # obj.absolute_url()
        
    #https://www.uwosh.edu/streaming-videos/streams/kan5693865-4693866/@@images/image
    

def ResourceEnhancer(id, title):

    data = {
        'id' : CleanID(id),
        'full_id' : id,
        'name' : '',
        'base_url' : '',
        'embed' : '',
    }
    
    if ALEXANDER_STREET_TARGET in id.lower():
        data['name'] = ALEXANDER_STREET_NAME
        data['base_url'] = 'https://www.remote.uwosh.edu/login?url=https://search.alexanderstreet.com/view/work/' + data['id']
        data['embed'] = '<iframe src="https://www.remote.uwosh.edu/login?url=https://search.alexanderstreet.com/embed/token/' + data['id'] + '" frameborder="0" allowfullscreen scrolling="no"></iframe>'
        
    elif KANOPY_TARGET in id.lower():
        data['name'] = KANOPY_NAME
        data['base_url'] = 'https://uwosh.kanopy.com/embed/' + data['id']
        data['embed'] = '<iframe allow="encrypted-media;" src="https://uwosh.kanopy.com/embed/' + data['id'] + '" frameborder="0" allowfullscreen webkitallowfullscreen mozallowfullscreen scrolling="no"></iframe>'
        
    elif FILMSONDEMAND_TARGET in id.lower():
        data['name'] = FILMSONDEMAND_NAME
        data['base_url'] = 'https://www.remote.uwosh.edu/login?url=http://fod.infobase.com/PortalPlaylists.aspx?wID=102638&xtid=' + data['id']
        data['embed'] = '<iframe frameborder="0" scrolling="no" src="https://www.remote.uwosh.edu/login?url=https://fod.infobase.com/OnDemandEmbed.aspx?token=' + data['id'] + '&wID=102638&plt=FOD&loid=0&w={WIDTH}&h={HEIGHT}&fWidth={WIDTH}&fHeight={HEIGHT}" allowfullscreen >&nbsp;</iframe>'
            
    elif SWANK_TARGET in id.lower():
        data['name'] = SWANK_NAME
        data['base_url'] = 'https://digitalcampus-swankmp-net.www.remote.uwosh.edu/uwo280545/#/play/' + data['id'] + '?watch=1'
        data['embed'] = ''
        
    elif ALMA_TARGET in id.lower():
        data['name'] = ALMA_NAME
        data['base_url'] = 'https://uw-primo.hosted.exlibrisgroup.com/primo-explore/fulldisplay?docid=' + data['id'] + '&context=L&vid=OSH&search_scope=OSH_ALL&tab=default_tab&lang=en_US'
        data['embed'] = ''
        
    return data
    
        
def CleanID(id):
    if SWANK_TARGET in id.lower():
        return id.replace('swa','') # NOTE: it looks base64, so w should not be possible
    elif ALEXANDER_STREET_TARGET in id.lower():
        return re.sub("\D", "", id)
    elif KANOPY_TARGET in id.lower():
        id = id.split('-').pop()
        return re.sub("\D", "", id)
    elif FILMSONDEMAND_TARGET in id.lower():
        return re.sub("\D", "", id).lstrip('1').lstrip('0')
    elif ALMA_TARGET in id.lower():
        return id
        
        
def escape_reserved(text):
    if text:
        return text.replace(u'"', u'\\\\"')
    return text
        
        
def remove_non_ascii(text):
    if text and type(text) != unicode:
        return text.decode('utf-8') #unidecode(text)
    elif text:
        return text
    return u''
    
    
def to_unicode(text):
    if text:
        return ftfy.fix_text(str(text).decode('utf-8')) #unidecode(text)
    return u''

def BrainsToCSV(brains):
    output = io.StringIO()
    
    writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    
    #filmID,content_type,creator,title,date_of_publication,runtime,series_title,summary,associated_entity,geography,subject,genre
    writer.writerow(['filmID','creator','title','date_of_publication','runtime','series_title','summary','format_type','associated_entity','geography','subject_group','genre','image_url','direct_url'])
    
    for brain in brains:
        row = []
        row.append(brain.getId)
        row.append(brain.creator)
        row.append(brain.Title)
        row.append(brain.date_of_publication)
        row.append(brain.runtime)
        row.append(list(brain.series_title))
        row.append(brain.Description)
        row.append(brain.format_type)
        row.append(list(brain.associated_entity))
        row.append(list(brain.geography))
        row.append(list(brain.subject_group))
        row.append(list(brain.genre))
        # row.append([ remove_non_ascii(x) for x in brain.series_title])
        # row.append(brain.Description)
        # row.append([ remove_non_ascii(x) for x in brain.associated_entity])
        # row.append([ remove_non_ascii(x) for x in brain.geography])
        # row.append([ remove_non_ascii(x) for x in brain.subject_group])
        # row.append([ remove_non_ascii(x) for x in brain.genre])
        row.append(brain.image_url)
        row.append(brain.getRemoteUrl)
        writer.writerow(row)
        
    contents = output.getvalue()
    output.close()
    return contents
        
    
    
def text_to_tuple(text):
    if type(text) is tuple:
        return text
    lines = text.replace(u'\r', u'').split(u'\n')
    if len(lines) == 0 or lines[0] == u'':
        return ()
    return tuple(lines)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        