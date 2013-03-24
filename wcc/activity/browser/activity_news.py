from five import grok
from plone.directives import dexterity, form
from wcc.activity.content.activity import IActivity
from Products.Archetypes.interfaces.referenceable import IReferenceable
from Products.ATContentTypes.interfaces.news import IATNewsItem
from Products.CMFPlone.PloneBatch import Batch

grok.templatedir('templates')

class NewsListingView(dexterity.DisplayForm):
    grok.context(IActivity)
    grok.require('zope2.View')
    grok.template('activity_news')
    grok.name('activity_news')

    def update(self):
        refs = IReferenceable(self.context)
        self.items = [n for n in refs.getBRefs() if IATNewsItem.providedBy(n)]

    def batch(self):
        b_start = self.request.get('b_start', 0)
        b_size = 10
        return Batch(self.items, b_size, int(b_start), orphan=0)
