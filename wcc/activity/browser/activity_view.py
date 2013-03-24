from five import grok
from plone.directives import dexterity, form
from wcc.activity.content.activity import IActivity
from Products.Archetypes.interfaces.referenceable import IReferenceable
from wcc.activity.interfaces import IActivityRelation
grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IActivity)
    grok.require('zope2.View')
    grok.template('activity_view')
    grok.name('view')

    def related_news(self):
        rels = IActivityRelation(self.context)
        return rels.related_news()[:3]
