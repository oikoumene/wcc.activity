from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from Products.Archetypes import atapi
from Products.ATContentTypes.interfaces import IATContentType
from zope.interface import Interface
from five import grok
from wcc.activity.interfaces import IProductSpecific, IActivityTagEnabled
from wcc.activity import MessageFactory as _
from archetypes.referencebrowserwidget import ReferenceBrowserWidget
# Visit http://pypi.python.org/pypi/archetypes.schemaextender for full 
# documentation on writing extenders

class ExtensionReferenceField(ExtensionField, atapi.ReferenceField):
    pass

class ActivityTag(grok.Adapter):

    # This applies to all AT Content Types, change this to
    # the specific content type interface you want to extend
    grok.context(IActivityTagEnabled)

    grok.implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    grok.provides(IOrderableSchemaExtender)
    grok.name('wcc.activity.activitytag')

    layer = IProductSpecific

    fields = [
        # add your extension fields here
        ExtensionReferenceField('related_activities',
            multiValued=True,
            required=False,
            relationship='ActivityTag',
            allowed_types=('wcc.activity.activity',),
            widget=ReferenceBrowserWidget(
                label='Related Activities',
                allow_browse=False,
                show_results_without_query=True,
                )
        )
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

    def getOrder(self, schematas):
        # you may reorder the fields in the schemata here
        return schematas
