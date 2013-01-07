from collective.grok import gs
from wcc.activity import MessageFactory as _

@gs.importstep(
    name=u'wcc.activity', 
    title=_('wcc.activity import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('wcc.activity.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
