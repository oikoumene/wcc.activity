from five import grok
from wcc.activity.interfaces import IActivityRelation
from wcc.activity.content.activity import IActivity

grok.templatedir('templates')

class ActivityNewsRSS(grok.View):
    grok.template('activity_news_rss')
    grok.name('RSS')
    grok.context(IActivity)

    def feeditems(self):
        return IActivityRelation(self.context).related_news()[:20]
