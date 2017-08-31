from plone import api
from plone.memoize import ram
from plone.i18n.normalizer import idnormalizer
from StringIO import StringIO
from unidecode import unidecode
import re, time

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
        data['base_url'] = 'https://uwosh.kanopystreaming.com/embed/' + data['id']
        data['embed'] = '<iframe src="https://uwosh.kanopystreaming.com/embed/' + data['id'] + '" frameborder="0" allowfullscreen webkitallowfullscreen mozallowfullscreen scrolling="no"></iframe>'
        
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
        
        
def remove_non_ascii(text):
    return unidecode(text)

def BrainsToCSV(brains):
    output = StringIO()
    #filmID,content_type,creator,title,date_of_publication,runtime,series_title,summary,associated_entity,geography,subject,genre
    output.write('filmID,content_type,creator,title,date_of_publication,runtime,series_title,summary,associated_entity,geography,subject,genre,image_url\n')
    
    for brain in brains:
    
        output.write(brain.getId)
        output.write(',')
        output.write(brain.content_type)
        output.write(',"')
        output.write(remove_non_ascii(brain.creator))
        output.write('","')
        output.write(remove_non_ascii(brain.Title))
        output.write('","')
        output.write(brain.date_of_publication)
        output.write('","')
        output.write(brain.runtime)
        output.write('","')
        output.write(str([ str(remove_non_ascii(x)) for x in brain.series_title]))
        output.write('","')
        output.write(remove_non_ascii(brain.Description))
        output.write('","')
        output.write(str([ str(remove_non_ascii(x)) for x in brain.associated_entity]))
        output.write('","')
        output.write(str([ str(remove_non_ascii(x)) for x in brain.geography]))
        output.write('","')
        output.write(str([ str(remove_non_ascii(x)) for x in brain.subject]))
        output.write('","')
        output.write(str([ str(remove_non_ascii(x)) for x in brain.genre]))
        output.write('","')
        output.write(brain.image_url)
        output.write('"\n')

    contents = output.getvalue()
    output.close()
    return contents
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        