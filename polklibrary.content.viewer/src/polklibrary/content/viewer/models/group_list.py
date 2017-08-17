from plone import api
from plone.supermodel import model
from zope import schema
from zope.interface import directlyProvides
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary

def collection_vocab(context):
    try:
        voc = []
        brains = api.content.find(portal_type='polklibrary.content.viewer.models.collection', sort_on='sortable_title')
        for brain in brains:
            voc.append(SimpleVocabulary.createTerm(brain.getId, brain.getId, brain.Title))
        return SimpleVocabulary(voc)
    except Exception as e:
        return []
directlyProvides(collection_vocab, IContextSourceBinder)


class IGroupList(model.Schema):

    title = schema.TextLine(
            title=u"Title",
            required=True,
        )

    description = schema.Text(
            title=u"Description",
            required=False,
        )

    collections = schema.List(
            title=u"Show Collections (also orders list)",
            required=False,
            value_type=schema.Choice(source=collection_vocab),
        )
        