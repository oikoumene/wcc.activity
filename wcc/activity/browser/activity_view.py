from five import grok
from plone.directives import dexterity, form
from wcc.activity.content.activity import IActivity
from Products.Archetypes.interfaces.referenceable import IReferenceable
from wcc.activity.interfaces import IActivityRelation
grok.templatedir('templates')
import datetime

class Index(dexterity.DisplayForm):
    grok.context(IActivity)
    grok.require('zope2.View')
    grok.template('activity_view')
    grok.name('view')

    def update(self):
        self.rels = IActivityRelation(self.context)

    def related_news(self):
        return self.rels.related_news()[:3]
    
    def related_events(self):
        items = self.rels.related_events()
        current = datetime.datetime.now().strftime("%Y-%m-%d %H:%m")
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
        
        return objects[:3]

    def related_documents(self):
        return self.rels.related_documents()[:3]
