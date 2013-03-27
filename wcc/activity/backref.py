# http://code.google.com/p/dexterity/issues/detail?id=234

from Acquisition import aq_inner
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from zc.relation.interfaces import ICatalog
from plone.multilingualbehavior.interfaces import IDexterityTranslatable
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner
from zope.component import queryAdapter
from plone.multilingual.interfaces import ITranslationManager
from plone.multilingual.interfaces import ILanguage
from Products.Archetypes.interfaces.referenceable import IReferenceable
from archetypes.multilingual.interfaces import IArchetypesTranslatable
from plone.multilingual.interfaces import ITranslatable

def back_references(source_object, attribute_name):
    """ Return back references from source object on specified attribute_name """
    catalog = getUtility(ICatalog)
    intids = getUtility(IIntIds)
    language_tool = getToolByName(source_object, 'portal_languages')
    default_language = language_tool.getDefaultLanguage()

    result = []
    # if this object is translatable, we should get the back relationship from the
    # default language of this object
    if IDexterityTranslatable.providedBy(source_object):
        trans_manager = ITranslationManager(aq_inner(source_object))
        trans_obj = trans_manager.get_translation(default_language)
        if trans_obj:
            source_object = trans_obj

    for rel in catalog.findRelations({
            'to_id': intids.getId(aq_inner(source_object)),
            'from_attribute':attribute_name
        }):
        obj = intids.queryObject(rel.from_id)
        if obj is not None and checkPermission('zope2.View', obj):
            if ITranslatable.providedBy(obj):
                lang = queryAdapter(obj, ILanguage).get_language()
                trans_manager = ITranslationManager(aq_inner(obj))
                trans_obj = trans_manager.get_translation(lang)
                if trans_obj:
                    result.append(trans_obj)
                    continue

            result.append(obj)
    return result

def at_back_references(source_object, relationship):
    language_tool = getToolByName(source_object, 'portal_languages')
    default_language = language_tool.getDefaultLanguage()

    # if this object is translatable, we should get the back relationship from the
    # default language of this object

    if IArchetypesTranslatable.providedBy(source_object):
        trans_manager = ITranslationManager(aq_inner(source_object))
        trans_obj = trans_manager.get_translation(default_language)
        if trans_obj:
            source_object = trans_obj

    refs = IReferenceable(source_object).getBRefs(relationship=relationship)
    
    result = []
    for obj in refs:
        if ITranslatable.providedBy(obj):
            lang = queryAdapter(obj, ILanguage).get_language()
            trans_manager = ITranslationManager(aq_inner(obj))
            trans_obj = trans_manager.get_translation(lang)
            if trans_obj:
                result.append(trans_obj)
                continue
        result.append(obj)

    return result
