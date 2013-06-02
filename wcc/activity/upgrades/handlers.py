from collective.grok import gs
from Products.CMFCore.utils import getToolByName
import logging
logger = logging.getLogger("wcc.activity")
from wcc.activity.interfaces import IActivityTagEnabled
from wcc.activity.content.activity import IActivity
from zope.lifecycleevent import ObjectModifiedEvent
from zope.event import notify
from Acquisition import aq_base
from Products.ATContentTypes.interfaces.news import IATNewsItem
from Acquisition import aq_base
# -*- extra stuff goes here -*- 


@gs.upgradestep(title=u'Upgrade wcc.activity to 1006',
                description=u'Upgrade wcc.activity to 1006',
                source='1005', destination='1006',
                sortkey=1, profile='wcc.activity:default')
def to1006(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-wcc.activity.upgrades:to1006')

    catalog = getToolByName(context, 'portal_catalog')

    for brain in catalog(portal_type='wcc.activity.activity', Language='all'):
        obj = brain.getObject()
        if getattr(aq_base(obj), 'image', None):
            if not obj.image.data:
                aq_base(obj).image = None
        else:
            aq_base(obj).image = None




@gs.upgradestep(title=u'Upgrade wcc.activity to 1005',
                description=u'Upgrade wcc.activity to 1005',
                source='1004', destination='1005',
                sortkey=1, profile='wcc.activity:default')
def to1005(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-wcc.activity.upgrades:to1005')

    catalog = getToolByName(context, 'portal_catalog')

    for brain in catalog(portal_type='wcc.activity.activity'):
        obj = brain.getObject()
        if getattr(aq_base(obj), 'image', None):
            if not obj.image.data:
                aq_base(obj).image = None
        else:
            aq_base(obj).image = None


@gs.upgradestep(title=u'Upgrade wcc.activity to 1004',
                description=u'Upgrade wcc.activity to 1004',
                source='1003', destination='1004',
                sortkey=1, profile='wcc.activity:default')
def to1004(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-wcc.activity.upgrades:to1004')
_marker = []

@gs.upgradestep(title=u'Upgrade wcc.activity to 1003',
                description=u'Upgrade wcc.activity to 1003',
                source='1002', destination='1003',
                sortkey=1, profile='wcc.activity:default')
def to1003(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-wcc.activity.upgrades:to1003')

    catalog = getToolByName(context, 'portal_catalog')
    catalog.reindexIndex('object_provides', context.REQUEST)

    for brain in catalog(object_provides=IActivityTagEnabled.__identifier__,
            Language='en'):
        obj = brain.getObject()
        try:
            notify(ObjectModifiedEvent(obj))
        except UnicodeDecodeError:
            continue

    for brain in catalog(object_provides=IActivity.__identifier__,
            Language='all'):
        obj = brain.getObject()
        img = getattr(aq_base(obj), 'image', _marker)
        if img is _marker:
            aq_base(obj).image = None


@gs.upgradestep(title=u'Upgrade wcc.activity to 1002',
                description=u'Upgrade wcc.activity to 1002',
                source='1001', destination='1002',
                sortkey=1, profile='wcc.activity:default')
def to1002(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-wcc.activity.upgrades:to1002')

    # apply referenceable behavior

    # See plone.app.referenceablebehavior.uidcatalog.
    uid_catalog = getToolByName(context, 'uid_catalog')
    portal_catalog = getToolByName(context, 'portal_catalog')
    brains = portal_catalog(portal_type='wcc.activity.activity')
    for brain in brains:
        obj = brain.getObject()
        path = '/'.join(obj.getPhysicalPath())
        logger.info("Applying referenceable behavior for object at path %s", 
                path)
        uid_catalog.catalog_object(obj, path)


@gs.upgradestep(title=u'Upgrade wcc.activity to 1001',
                description=u'Upgrade wcc.activity to 1001',
                source='1', destination='1001',
                sortkey=1, profile='wcc.activity:default')
def to1001(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-wcc.activity.upgrades:to1001')
