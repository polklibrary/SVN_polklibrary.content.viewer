from plone import api
from plone.i18n.normalizer import idnormalizer
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility, getMultiAdapter
from zope.container.interfaces import INameChooser
from polklibrary.content.viewer.utility import BrainsToCSV
import csv, io, re, ast, json
import pprint, ftfy, logging

logger = logging.getLogger("Plone")



class ExporterView(BrowserView):

    output = ""
    
    def __call__(self):
        self.request.response.setHeader("Content-Disposition", "attachment;filename=export.csv")
        catalog = api.portal.get_tool(name='portal_catalog')
        brains = catalog.searchResults(
            portal_type='polklibrary.content.viewer.models.contentrecord',
            review_state='published'
        )
        return BrainsToCSV(brains)

