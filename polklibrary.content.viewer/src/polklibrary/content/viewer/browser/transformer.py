from plone import api
from plone.i18n.normalizer import idnormalizer
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility, getMultiAdapter
from zope.container.interfaces import INameChooser
from polklibrary.content.viewer.marc_utility import build_rec

import io, re, ast, json
import pprint, ftfy, logging, csv

logger = logging.getLogger("Plone")


def unicode_csv_reader(utf8_data, delimiter=',', quotechar='"', dialect=csv.excel):
    csv_reader = csv.reader(utf8_data, delimiter=delimiter, quotechar=quotechar, dialect=dialect)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]
        


class TransformerView(BrowserView):

    template = ViewPageTemplateFile("templates/transformer.pt")
    error = None

    def __call__(self):
        self.file = self.request.get('form.file.upload', None)
        if self.file:
            new_filename = self.file.filename.replace('.mrc','') + '.csv'
            if self.request.get('form.file.allcsv', None):
                csv_data = self.transform_marc_to_csv(False)
                self.request.response.setHeader("Content-type", "application/csv")
                self.request.response.setHeader("Content-Disposition", "attachment;filename=" + new_filename);
                self.request.response.setBody(csv_data, lock=True)
            if self.request.get('form.file.idcsv', None):
                csv_data = self.transform_marc_to_csv(True)
                self.request.response.setHeader("Content-type", "application/csv")
                self.request.response.setHeader("Content-Disposition", "attachment;filename=" + new_filename);
                self.request.response.setBody(csv_data, lock=True)
            
        return self.template()


    def transform_marc_to_csv(self, id_only):
        #input_stream = io.StringIO(self.file.read())
        input_stream = io.StringIO(self.file.read().decode("utf-8"))
        subj, geo, topics = build_rec(input_stream)
        name = 'done.csv'
        #with open(name, mode='wb') as f:
        #outputstream = io.StringIO(self.file.read())
        outputstream = io.StringIO(self.file.read().decode("utf-8"))
        w = csv.writer(outputstream, encoding='utf-8')
        for row in subj:
            if len(row) > 0:
                if id_only:
                    w.writerow([row[0]]) 
                else:
                    w.writerow(row)  
        return outputstream.getvalue()
        
    @property
    def portal(self):
        return api.portal.get()
    