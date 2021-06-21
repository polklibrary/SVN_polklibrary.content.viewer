from pymarc import MARCReader
from geotext import GeoText
import sys
#import unicodecsv as csv
import csv

#file = sys.argv[1]

#exclude_file = 'country_homophones.txt'

global country_homophones
country_homophones = ['Bury','March','Marks','Graham','Bo','Rosenberg','Graham','University','Kansas','Lawrence','Allen','Eugene','Brecht','Bentley','Man','Warren','Most','Regina','Cork','Highland','Flores','Elizabeth','Marshall','Americana','Police','Young','Wilson','Of','Fishers','Darwin','Martin','Bradford','Spring','Pop','Born','Bear','Mary','Bell','Mao','Temple','Along','Sherman','Much','Quincy','Paris','Paradise','Roman','Chor','Guilford','Johnson','Latina','Jackson','Summit','Gay','Male','Federal','Eden','Chekhov','Hayes','Reading','Boom','Barking','Tara','Alice','Harper','Barry','Nigel','Dale','Gary','David','Best','Split','Anna','Fleet','Pen','Carol','Lynn','Alicia','Nikki','Donna','Stuart','George','SIM','Sale','Enterprise','Charlotte','Barking','Tracy','Peer','PISA','Clive','Salt','Roy','Howard','Estelle','Helena','Working','Vic','Euclid','Allende','Normal','Asia','Obama','Iowa','Bronte','Nancy','Lakota','Melville','Rosario','Brad','Union','Liberty','Independence','Asia','Hercules','Wright','Clinton','Roman','Lucas','Savage','Goes','Gap','Jupiter','Taylor','Orion','Natal','Badger','Leatherhead','Roses','Batman','Griffith','Parker','Van','Rogers','Vista','Mustang','Montana','Chelsea','Mission','Dalton','Buy','Toledo','Gilbert','Evans','Oregon','Kansas','ABA','Bay','Tours','Leer','Sunrise','Imperial','Palm','The Valley','Dublin','Fountain','Kant','Plato','Ho','Norman','Bath','Honda','Toyota','Keller','Rye','Walker','Foster','Linda','Pace','Ode','Milton','Moss','Parole','Bar','Holden','Pearl','Lens','Date','Orange','Walnut','Atlantis','Davis','Homestead','Roth','Irving','OSA','UN','Green','Amos','Kyle','Palmer','Mon','Nice','Defiance','Wedding','Tire','Ron','Griffin','AUSA','Arnold','Bradley','Sebastian','Moe','Dome','Lice','Shaping','Bowie','Country Club','Bra','Central','Hull','Murray','Vincent','Anderson','Baron','Brits','Gardner','Ripley','Ariel','Lincoln','Opportunity','Oral','Manage','Sandy','Ramon','Converse','Gallup','Crystal','Humble','Wa','Mobile','Carson','Manga','Oss','Taft','Aloha','Crosby','Boo','Murphy','Gay','Newton','Moore','Inca','Perm','Ada','Metro','Eagle','Swords','Plunge','Derby','Hickory','Antony','Bryan','Cary','Beacon','Pinto','Turbo','Bartlett','Duncan','Vladimir','Mercedes','Bountiful','Dole','Sake','Edison','Stanley']

#returns formatted string from pymarc field 
def format_pymarc(i):
    try:
        text = i[0]
        return text.format_field()
    except AttributeError:
        return ''
    except IndexError:
        return ''
#get geographic subdividsions from subject headings 
def read_geo_sub(record):
    try:
        geo_div = record['650']['z']
        geo_div = geo_div.replace('.', '')
        return geo_div 
    except TypeError:
        pass
    except AttributeError:
        pass 
#get geographic subdividsions pt 2 
def read_geo_head(record):
    try:
        geo_head = record['651']['a']
        geo_head = geo_head.replace('.', '')
        return geo_head 
    except TypeError:
        pass    
    except AttributeError:
        pass 
#isolates topical terms in MARC subject headings 
def read_topic(record):
    topics = []
    subj_list = record.get_fields('650')
    for i in subj_list:
        str = i.format_field()
        if '--' in str:
            tmp = str.split('--')
            topics.append(tmp[0].strip())
        else:
            topics.append(str)
    return topics         
#test to see if a particular marc field is in record 
def presence_test(rec, field, subfield):
    try:
        val = rec[field][subfield]
        if val is not None:
            return val
        else:
            return ''
    except TypeError:
        return ''
#read a text file (not needed) 
def read_text(f):
    out = []
    with open(f, 'r') as rf:
        reader = csv.reader(rf)
        for i in reader:
            out.append(i)
    return out         
#remove particular substrings in list from a given string         
def remove_substring(s, list):
    for i in list:
        s = s.replace(i, '')
    return s

#takes MARC record and returns csv file to be added to streaming video site 
    
def build_rec(stream):
    #exclude = [m for sub in exclude for m in sub]
    global country_homophones
    exclude = country_homophones
    #print(exclude[0:10])
    strip_list = ['1 online resource', '(', ')', '1 video file', '1 streaming video file', '1 streaming', 'video', 'stereo', 'file', 'online resource','sound', 'digital', 'flv', 'online', 'color', 'and', 'streaming video file','streaming video files', '+', 'instructional', 'materials', 'sd', 'col', 'sd col digital file', '1 streaming video', '1 electronic resource', 'streaming', 'approximately', ',', '.', ':']
    genre_strip = ['lcgft','Internet videos.', 'Videorecording']
    out_list = []
    count = 0
    geo_list = []
    geo_headings = []
    topics = []
    has_geo = 0
    #header = ['filmID', 'creator', 'title', 'date', 'phys_desc', 'series', 'summary', 'subj_person', 'subj_corp', 'rec_topics', 'rec_geo', 'genre', 'subj_person2']
    header = ['filmID', 'creator', 'title', 'date_of_publication', 'runtime', 'series_title', 'summary', 'content_type', 'associated_entity', 'geography', 'subject', 'genre']
    out_list.append(header)
    #with open(stream, 'rb') as rf:
    reader = MARCReader(stream, to_unicode=True)
    for rec in reader:
        rec_geo = []
        count += 1
        vendor_name = ''
        if count % 10000 == 0:
            print('on record #' + str(count))
        id = format_pymarc(rec.get_fields('001')).lower()
        auth = format_pymarc(rec.get_fields('100'))
        title = presence_test(rec, '245', 'a')
        sub_title = presence_test(rec, '245', 'b')
        part = presence_test(rec, '245', 'n')
        number = presence_test(rec, '245', 'p')
        date = presence_test(rec, '260', 'c')
        title = title + ' ' + sub_title + ' ' + number + ' ' + part
        title = title.replace('/', '')
        tmp_title = title 
        phys_desc = format_pymarc(rec.physicaldescription())
        phys_desc = remove_substring(phys_desc, strip_list)
        series = format_pymarc(rec.get_fields('490'))
        
        if len(number) > 0 and len(series) == 0:
            series = tmp_title
            title.replace(series, '')
        elif len(part) > 0 and len(series) == 0:
            series = tmp_title
            title.replace(series, '')
        if ';' in series:
            x = series.split(';')
            series_name = x[0]
            part_num = x[1]
            title = title + ' ' + series_name + ' ' + part_num
            series = series_name    
        summary = format_pymarc(rec.get_fields('520'))
        geo_text = GeoText(summary)
        cities = geo_text.cities
        for i in cities:
            if i not in exclude:
                rec_geo.append(i)        
        countries = list(geo_text.country_mentions)
        geo_cities = [cities, countries] 
        subj_person = format_pymarc(rec.get_fields('600'))
        subj_person = subj_person.replace('.', '')
        subj_corp = format_pymarc(rec.get_fields('610'))
        rec_topics = read_topic(rec)
        rec_topics = [i.replace('.', '') for i in rec_topics]
        set_rec_topics = set(rec_topics)
        rec_topics = list(set_rec_topics)
        if rec_topics is not None:
            topics.append(rec_topics)
        geo_terms = read_geo_sub(rec)
        if geo_terms is not None:
            geo_list.append(geo_terms)
            rec_geo.append(geo_terms)            
        geo_head = read_geo_head(rec)
        if geo_head is not None:
            geo_list.append(geo_head)
            rec_geo.append(geo_head)
        geo = format_pymarc(rec.get_fields('651'))
        genre = format_pymarc(rec.get_fields('655'))
        genre = remove_substring(genre, genre_strip)
        subj_person2 = format_pymarc(rec.get_fields('700'))
        rec_geo = list(set(rec_geo))
        
        url = rec['856']['u']
        try:
            id_test = int(id)
            id = 'fod' + id 
        except ValueError:
            if 'kan' in id:
                vendor_name = 'kanopy'
                id2 = url.split('/')[-1]
                id = id + '-' + id2 
            if 'asp' in id:
                vendor_name = 'astreet'        
        associated_entities = subj_person + subj_corp        
        tmp = [id, auth, title.strip(), date.strip(), phys_desc.strip(), series.strip(), summary.strip(), 'stream', associated_entities, rec_geo, rec_topics, genre]
            #['filmID', 'creator', 'title', 'date_of_publication', 'runtime', 'series_title', 'summary', 'content_type', 'associated_entity', 'geography', 'subject', 'genre']
        if '/aamr' not in id:
            out_list.append(tmp)

    return out_list, geo_list, topics           
                
def search_summary(tup):
    summary = tup[1]
    subj = tup[0]
    all_terms = []
    for v in subj:
        if '--' in v:
            tmp = v.split('--')
            for x in tmp:
                x = x.replace('.', '')
                all_terms.append(x)
        else:
            v = v.replace('.', '')
            all_terms.append(v)
    match_count = 0        
    for item in all_terms:
        if item in summary:
            match_count += 1
        
    final = [summary, subj, match_count]
    return final  
    
    
def pymarc_test(f):
    with open(f, 'rb') as rf:
        reader = MARCReader(rf)
        for rec in reader:
            try:
                x = rec['651']['a']
                print(x)
            except TypeError:
                pass

def write_results(l):
    #name = input('name your out file\n')
    #name = name + '.csv'
    name = 'done.csv'
    with open(name, mode='wb') as f:
        w = csv.writer(f, encoding='utf-8')
        for row in l:
            if len(row) > 0:
                w.writerow(row)                

def write_dict(d,s):
    with open(s, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['subject heading', 'total ct', 'astreet ct', 'kanopy ct', 'fod ct', 'unknown ct'])
        for k, v in d.items():
            cts = v
            tmp = [k, cts[0], cts[1], cts[2], cts[3], cts[4]]
            w.writerow(tmp)
            


    
# def main():
    # exclude = read_text(exclude_file)
    # subj, geo, topics  = build_rec(file, exclude)
    # print('geo terms detected: ' + str(len(geo)))
    # print('topic terms detected: ' + str(len(topics)))
    # write_results(subj)
    
# main()
                
            
            
            
            
            
            
            
