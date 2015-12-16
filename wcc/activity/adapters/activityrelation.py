from five import grok
from wcc.activity.content.activity import IActivity
from wcc.activity.interfaces import IActivityRelation
from Products.Archetypes.interfaces.referenceable import IReferenceable
from wcc.activity.backref import back_references, at_back_references
from Products.ATContentTypes.interfaces.news import IATNewsItem
from Products.ATContentTypes.interfaces.file import IATFile
from Products.ATContentTypes.interfaces.folder import IATFolder
from wcc.document.content.document import IDocument
from plone.multilingual.interfaces import ITranslatable
from plone.multilingual.interfaces import ILanguage
from zope.component import queryAdapter
from Products.ATContentTypes.interfaces.event import IATEvent

class ActivityRelationAdapter(grok.Adapter):
    grok.implements(IActivityRelation)
    grok.context(IActivity)

    def __init__(self, context):
        self.context = context
        self._atrefs = at_back_references(context, 'ActivityTag')
        self._dexterityrefs = back_references(context, 'related_activities')
        self.refs = sorted(self._atrefs + self._dexterityrefs,
                key=lambda x:x.Date(), reverse=True)

    def related_news(self):
        result = []
        curr_lang = queryAdapter(self.context, ILanguage).get_language()
        for i in self.refs:
            if IATNewsItem.providedBy(i):
                item_lang = queryAdapter(i, ILanguage).get_language()
                if item_lang == curr_lang:
                    result.append(i)
        return result
    
    def related_events(self):
        result = []
        curr_lang = queryAdapter(self.context, ILanguage).get_language()
        for i in self.refs:
            if IATEvent.providedBy(i):
                item_lang = queryAdapter(i, ILanguage).get_language()
                if item_lang == curr_lang:
                    result.append(i)
        return result

    def related_documents(self):
        return [i for i in self.refs if self._is_document(i)]

    def _is_document(self, item):
        if IATNewsItem.providedBy(item):
            return False
        if IDocument.providedBy(item):
            return True
        if IATFile.providedBy(item):
            return True
        if IATFolder.providedBy(item):
            return True
        return False
