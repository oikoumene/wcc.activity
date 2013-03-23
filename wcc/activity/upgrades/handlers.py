from collective.grok import gs
from Products.CMFCore.utils import getToolByName
import logging
logger = logging.getLogger("wcc.activity")
# -*- extra stuff goes here -*- 


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
