from five import grok
from plone.directives import dexterity, form
from wcc.activity.content.activity import IActivity
from Products.Archetypes.interfaces.referenceable import IReferenceable
from Products.ATContentTypes.interfaces.news import IATNewsItem
from Products.CMFPlone.PloneBatch import Batch
from wcc.activity.interfaces import IActivityRelation

grok.templatedir('templates')

class EventsListingView(dexterity.DisplayForm):
    grok.context(IActivity)
    grok.require('zope2.View')
    grok.template('activity_events')
    grok.name('activity_events')

    def update(self):
        rels = IActivityRelation(self.context)
        self.items = rels.related_events()

    def batch(self):
        b_start = self.request.get('b_start', 0)
        b_size = 10
        return Batch(self.items, b_size, int(b_start), orphan=0)
