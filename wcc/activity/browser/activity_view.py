from five import grok
from plone.directives import dexterity, form
from wcc.activity.content.activity import IActivity
from Products.Archetypes.interfaces.referenceable import IReferenceable

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IActivity)
    grok.require('zope2.View')
    grok.template('activity_view')
    grok.name('view')

    def related_news(self):
        refs = IReferenceable(self.context)
        return refs.getBRefs()[:5]
