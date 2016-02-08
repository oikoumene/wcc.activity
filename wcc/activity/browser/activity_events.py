from five import grok
from plone.directives import dexterity, form
from wcc.activity.content.activity import IActivity
from Products.Archetypes.interfaces.referenceable import IReferenceable
from Products.ATContentTypes.interfaces.news import IATNewsItem
from Products.CMFPlone.PloneBatch import Batch
from wcc.activity.interfaces import IActivityRelation
import datetime

grok.templatedir('templates')

class EventsListingView(dexterity.DisplayForm):
    grok.context(IActivity)
    grok.require('zope2.View')
    grok.template('activity_events')
    grok.name('activity_events')

    def update(self):
        rels = IActivityRelation(self.context)
        self.items = rels.related_events()

    def batch_2(self):
        b_start = self.request.get('b_start', 0)
        b_size = 10
        return Batch(self.items, b_size, int(b_start), orphan=0)
    
    def batch(self):
        b_start = self.request.get('b_start', 0)
        b_size = 10
        current = datetime.datetime.now().strftime("%Y-%m-%d %H:%m")
        items = self.items
        brains = []
        objects = []
        if items:
            for item in items:
                if item.start_date and item.end_date:
                    if item.start_date.strftime("%Y-%m-%d %H:%m") >= current  or current <= item.end_date.strftime("%Y-%m-%d %H:%m"):
                        brains.append({'start':item.start_date.strftime("%Y-%m-%d %H:%m"), 'obj':item})
        if brains:
            brains.sort(key=lambda val: val['start'])
            objects = [x['obj'] for x in brains]
        
        return Batch(objects, b_size, int(b_start), orphan=0)
        
