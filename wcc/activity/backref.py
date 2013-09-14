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
from AccessControl import getSecurityManager
from AccessControl import Unauthorized

def back_references(source_object, attribute_name):
    """ Return back references from source object on specified attribute_name """
    language_tool = getToolByName(source_object, 'portal_languages')
    default_language = language_tool.getDefaultLanguage()

    default_rels = []
    # if this object is translatable, we should get the back relationship from the
    # default language of this object
    if ITranslatable.providedBy(source_object):
        trans_manager = ITranslationManager(aq_inner(source_object))
        default_lang_obj = trans_manager.get_translation(default_language)
        if default_lang_obj:
            default_rels = _back_references(default_lang_obj, attribute_name, source_object)

    return list(set(default_rels + _back_references(source_object, attribute_name)))

def _back_references(source_object, attribute_name, translation=None):
    catalog = getUtility(ICatalog)
    intids = getUtility(IIntIds)

    lang = queryAdapter(source_object, ILanguage).get_language()
    if translation:
        lang = queryAdapter(translation, ILanguage).get_language()

    gsm = getSecurityManager()
    result = []
    for rel in catalog.findRelations({
            'to_id': intids.getId(aq_inner(source_object)),
            'from_attribute':attribute_name
        }):
        obj = intids.queryObject(rel.from_id)
        if obj is not None and checkPermission('zope2.View', obj):
            if ITranslatable.providedBy(obj):
                trans_manager = ITranslationManager(aq_inner(obj))
                try:
                    trans_obj = trans_manager.get_translation(lang)
                except Unauthorized, e:
                    continue

                if trans_obj:
                    result.append(trans_obj)
                    continue

            if gsm.checkPermission('zope2.View', obj):
                result.append(obj)
    return result



def at_back_references(source_object, relationship):
    language_tool = getToolByName(source_object, 'portal_languages')
    default_language = language_tool.getDefaultLanguage()

    # if this object is translatable, we should get the back relationship from the
    # default language of this object

    default_rels = []
    if ITranslatable.providedBy(source_object):
        trans_manager = ITranslationManager(aq_inner(source_object))
        default_lang_obj = trans_manager.get_translation(default_language)
        if default_lang_obj:
            default_rels = _at_back_references(default_lang_obj, relationship, source_object)

    return list(set(default_rels + _at_back_references(source_object, relationship)))

def _at_back_references(source_object, relationship, translation=None):

    lang = queryAdapter(source_object, ILanguage).get_language()
    if translation:
        lang = queryAdapter(translation, ILanguage).get_language()

    refs = IReferenceable(source_object).getBRefs(relationship=relationship)
    gsm = getSecurityManager()
    result = []
    for obj in refs:
        if ITranslatable.providedBy(obj):
            trans_manager = ITranslationManager(aq_inner(obj))
            try: 
                trans_obj = trans_manager.get_translation(lang)
            except Unauthorized:
                continue

            if trans_obj:
                result.append(trans_obj)
                continue

        if gsm.checkPermission('zope2.View', obj):
            result.append(obj)

    return result
