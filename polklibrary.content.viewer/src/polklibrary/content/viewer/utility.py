from plone.i18n.normalizer import idnormalizer
import re

# used elsewhere to target
ALEXANDER_STREET_NAME = 'Alexander Street'
KANOPY_NAME = 'Kanopy'
FILMSONDEMAND_NAME = 'Films on Demand'
ALMA_NAME = 'Catalog'

ALEXANDER_STREET_TARGET = 'asp'
KANOPY_TARGET = 'kan'
FILMSONDEMAND_TARGET = 'fod'
ALMA_TARGET = 'alma'

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
        data['embed'] = '<iframe src="https://www.remote.uwosh.edu/login?url=https://search.alexanderstreet.com/embed/token/' + data['id'] + '" frameborder="0" width="700" height="450" allowfullscreen scrolling="no"></iframe>'
        
    elif KANOPY_TARGET in id.lower():
        data['name'] = KANOPY_NAME
        data['base_url'] = 'https://uwosh.kanopystreaming.com/embed/' + data['id']
        data['embed'] = '<iframe width="700" height="450" src="https://uwosh.kanopystreaming.com/embed/' + data['id'] + '" frameborder="0" allowfullscreen webkitallowfullscreen mozallowfullscreen scrolling="no"></iframe>'
        
    elif FILMSONDEMAND_TARGET in id.lower():
        data['name'] = FILMSONDEMAND_NAME
        data['base_url'] = 'https://www.remote.uwosh.edu/login?url=http://fod.infobase.com/PortalPlaylists.aspx?wID=102638&xtid=' + data['id']
        data['embed'] = '<iframe frameborder="0" scrolling="no" width="700" height="450" src="https://www.remote.uwosh.edu/login?url=https://fod.infobase.com/OnDemandEmbed.aspx?token=' + data['id'] + '&wID=102638&plt=FOD&loid=0&w=480&h=340&fWidth=700&fHeight=450" allowfullscreen >&nbsp;</iframe>'
            
    elif ALMA_TARGET in id.lower():
        data['name'] = ALMA_NAME
        data['base_url'] = 'https://www.remote.uwosh.edu/login?url=http://fod.infobase.com/PortalPlaylists.aspx?wID=102638&xtid=' + data['id']
        data['embed'] = ''
    
    return data
    
        
def CleanID(id):
    if ALEXANDER_STREET_TARGET in id.lower():
        return re.sub("\D", "", id)
    elif KANOPY_TARGET in id.lower():
        id = id.split('-').pop()
        return re.sub("\D", "", id)
    else:
        return id.lstrip('1').lstrip('0')
        
        
    