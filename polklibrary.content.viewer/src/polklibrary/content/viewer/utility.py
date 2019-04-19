from plone import api
from plone.memoize import ram
from plone.i18n.normalizer import idnormalizer
from StringIO import StringIO
from unidecode import unidecode
#from polklibrary.content.viewer import unicodecsv
import re, time, ftfy, csv, unicodecsv

# used elsewhere to target
ALEXANDER_STREET_NAME = 'Alexander Street'
KANOPY_NAME = 'Kanopy'
FILMSONDEMAND_NAME = 'Films on Demand'
ALMA_NAME = 'Catalog'

ALEXANDER_STREET_TARGET = 'asp'
KANOPY_TARGET = 'kan'
FILMSONDEMAND_TARGET = 'fod'
ALMA_TARGET = 'uwi'

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
        data['base_url'] = 'https://www.remote.uwosh.edu/login?url=https://uwosh.kanopy.com/embed/' + data['id']
        data['embed'] = '<iframe allow="encrypted-media;" src="https://www.remote.uwosh.edu/login?url=https://uwosh.kanopy.com/embed/' + data['id'] + '?v=20190405" frameborder="0" allowfullscreen webkitallowfullscreen mozallowfullscreen scrolling="no"></iframe>'
        
    elif FILMSONDEMAND_TARGET in id.lower():
        data['name'] = FILMSONDEMAND_NAME
        data['base_url'] = 'https://www.remote.uwosh.edu/login?url=http://fod.infobase.com/PortalPlaylists.aspx?wID=102638&xtid=' + data['id']
        data['embed'] = '<iframe frameborder="0" scrolling="no" src="https://www.remote.uwosh.edu/login?url=https://fod.infobase.com/OnDemandEmbed.aspx?token=' + data['id'] + '&wID=102638&plt=FOD&loid=0&w={WIDTH}&h={HEIGHT}&fWidth={WIDTH}&fHeight={HEIGHT}" allowfullscreen >&nbsp;</iframe>'
            
    elif ALMA_TARGET in id.lower():
        data['name'] = ALMA_NAME
        data['base_url'] = 'https://uw-primo.hosted.exlibrisgroup.com/primo-explore/fulldisplay?docid=' + data['id'] + '&context=L&vid=OSH&search_scope=OSH_ALL&tab=default_tab&lang=en_US'
        data['embed'] = ''
        
    return data
    
        
def CleanID(id):
    if ALEXANDER_STREET_TARGET in id.lower():
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
    output = StringIO()
    
    writer = unicodecsv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    
    #filmID,content_type,creator,title,date_of_publication,runtime,series_title,summary,associated_entity,geography,subject,genre
    writer.writerow([u'filmID',u'content_type',u'creator',u'title',u'date_of_publication',u'runtime',u'series_title',u'summary',u'associated_entity',u'geography',u'subject',u'genre'])
    
    for brain in brains:
        row = []
        row.append(unicode(brain.getId))
        row.append(unicode(brain.content_type))
        row.append(unicode(brain.creator))
        row.append(brain.Title)
        row.append(unicode(brain.date_of_publication))
        row.append(unicode(brain.runtime))
        row.append(to_unicode([ remove_non_ascii(x) for x in brain.series_title]))
        row.append(brain.Description)
        row.append(to_unicode([ remove_non_ascii(x) for x in brain.associated_entity]))
        row.append(to_unicode([ remove_non_ascii(x) for x in brain.geography]))
        row.append(to_unicode([ remove_non_ascii(x) for x in brain.subject_heading]))
        row.append(to_unicode([ remove_non_ascii(x) for x in brain.genre]))
        writer.writerow(row)
        
    contents = output.getvalue()
    output.close()
    return contents
        
    
    
def text_to_tuple(text):
    if type(text) is tuple:
        return text
    lines = text.replace(u'\r', u'').split(u'\n')
    return tuple(lines)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        