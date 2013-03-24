from five import grok
from wcc.activity.content.activity import IActivity
from wcc.activity.interfaces import IActivityRelation
from Products.Archetypes.interfaces.referenceable import IReferenceable
from wcc.activity.backref import back_references
from Products.ATContentTypes.interfaces.news import IATNewsItem
from Products.ATContentTypes.interfaces.file import IATFile
from wcc.document.content.document import IDocument

class ActivityRelationAdapter(grok.Adapter):
    grok.implements(IActivityRelation)
    grok.context(IActivity)

    def __init__(self, context):
        self.context = context
        self._atrefs = IReferenceable(context).getBRefs()
        self._dexterityrefs = back_references(context, 'related_activities')
        self.refs = sorted(self._atrefs + self._dexterityrefs,
                key=lambda x:x.Date(), reverse=True)

    def related_news(self):
        return [i for i in self.refs if IATNewsItem.providedBy(i)]

    def related_documents(self):
        return [i for i in self.refs if self._is_document(i)]

    def _is_document(self, item):
        if IDocument.providedBy(item):
            return True
        if IATFile.providedBy(item):
            return True
        return False
