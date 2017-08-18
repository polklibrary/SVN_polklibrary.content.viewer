from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model

from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.interface import provider, directlyProvides
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


content_types = SimpleVocabulary([
    SimpleTerm(value=u'book', title=u'Book'),
    SimpleTerm(value=u'dvd', title=u'DVD'),
    SimpleTerm(value=u'game', title=u'Board Game'),
    SimpleTerm(value=u'stream', title=u'Streaming Video'),
])


@provider(IFormFieldProvider)
class IContentRecord(model.Schema):

    id = schema.TextLine(
            title=u"ID",
            required=True,
        )
    
    title = schema.TextLine(
            title=u"Title",
            required=True,
        )
        
    description = schema.Text(
            title=u"Description",
            required=False,
        )
        
    content_type = schema.Choice(
            title=u"Content Type",
            source=content_types,
            required=False,
        )

    creator = schema.TextLine(
            title=u"Creator",
            required=False,
        )  

    runtime = schema.TextLine(
            title=u"Runtime",
            required=False,
        )

    date_of_publication = schema.TextLine(
            title=u"Date of Publication",
            required=False,
        )  

    series_title = schema.Tuple(
        title=u'Series Title',
        required=False,
        value_type=schema.TextLine(),
        missing_value=(),
    )
    directives.widget(
        'series_title',
        AjaxSelectFieldWidget,
        vocabulary='polklibrary.content.viewer.vocabularies.SeriesTitleVocabularyFactory'
    )
    directives.read_permission(series_title='cmf.AddPortalContent')
    directives.write_permission(series_title='cmf.AddPortalContent')
    directives.omitted('series_title')
    directives.no_omit(IEditForm, 'series_title')
    directives.no_omit(IAddForm, 'series_title')
        
        
    # --- Categorization FieldSet ---
    model.fieldset(
        'categorizing',
        label=u'Categorization', 
        fields=['subject_heading', 'associated_entity', 'geography', 'genre'],
    )
        
    subject_heading = schema.Tuple(
        title=u'Subject Heading',
        required=False,
        value_type=schema.TextLine(),
        missing_value=(),
    )
    directives.widget(
        'subject_heading',
        AjaxSelectFieldWidget,
        vocabulary='polklibrary.content.viewer.vocabularies.SubjectHeadingVocabularyFactory'
    )
    directives.read_permission(subject_heading='cmf.AddPortalContent')
    directives.write_permission(subject_heading='cmf.AddPortalContent')
    directives.omitted('subject_heading')
    directives.no_omit(IEditForm, 'subject_heading')
    directives.no_omit(IAddForm, 'subject_heading')
    
    
    associated_entity = schema.Tuple(
        title=u'Associated Entity',
        required=False,
        value_type=schema.TextLine(),
        missing_value=(),
    )
    directives.widget(
        'associated_entity',
        AjaxSelectFieldWidget,
        vocabulary='polklibrary.content.viewer.vocabularies.AssociatedEntityVocabularyFactory'
    )
    directives.read_permission(associated_entity='cmf.AddPortalContent')
    directives.write_permission(associated_entity='cmf.AddPortalContent')
    directives.omitted('associated_entity')
    directives.no_omit(IEditForm, 'associated_entity')
    directives.no_omit(IAddForm, 'associated_entity')
    
        
    
    geography = schema.Tuple(
        title=u'Geography',
        required=False,
        value_type=schema.TextLine(),
        missing_value=(),
    )
    directives.widget(
        'geography',
        AjaxSelectFieldWidget,
        vocabulary='polklibrary.content.viewer.vocabularies.GeographyVocabularyFactory'
    )
    directives.read_permission(geography='cmf.AddPortalContent')
    directives.write_permission(geography='cmf.AddPortalContent')
    directives.omitted('geography')
    directives.no_omit(IEditForm, 'geography')
    directives.no_omit(IAddForm, 'geography')
    
    
    genre = schema.Tuple(
        title=u'Genre',
        required=False,
        value_type=schema.TextLine(),
        missing_value=(),
    )
    directives.widget(
        'genre',
        AjaxSelectFieldWidget,
        vocabulary='polklibrary.content.viewer.vocabularies.GenreVocabularyFactory'
    )
    directives.read_permission(genre='cmf.AddPortalContent')
    directives.write_permission(genre='cmf.AddPortalContent')
    directives.omitted('genre')
    directives.no_omit(IEditForm, 'genre')
    directives.no_omit(IAddForm, 'genre')
    
    
    # --- Image FieldSet ---
    model.fieldset(
        'imageset',
        label=u'Image', 
        fields=['image_url', 'image'],
    )
    
    
    image_url = schema.TextLine(
            title=u"Image URL",
            required=False,
        )
        
    image = NamedBlobImage(
            title=u"Image File",
            required=False,
        )
        
    
    # --- Stats FieldSet ---
    model.fieldset(
        'statset',
        label=u'Stats', 
        fields=['likes', 'visits'],
    )
    
    likes = schema.Int(
            title=u"Total Likes",
            default=0
        )
        
    visits = schema.Int(
            title=u"Total Visits",
            default=0
        )
        
        
        
        
        
        
        
        
        