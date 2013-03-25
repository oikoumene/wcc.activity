from zope.interface import alsoProvides, implements
from zope.component import adapts
from zope import schema
from plone.directives import form
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider

from plone.namedfile import field as namedfile
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder

from wcc.activity import MessageFactory as _
from z3c.relationfield.schema import RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from wcc.activity.content.activity import IActivity
from Acquisition import aq_base

class IActivityTag(form.Schema):
    """
       Marker/Form interface for ActivityTag
    """

    related_activities = RelationList(
        title=_(u'Related Activities'),
        required=False,
        value_type=RelationChoice(
            source=ObjPathSourceBinder(object_provides=IActivity.__identifier__)
        ),
        default=[]
    )

    # -*- Your Zope schema definitions here ... -*-

alsoProvides(IActivityTag,IFormFieldProvider)

class ActivityTag(object):
    """
       Adapter for ActivityTag
    """
    implements(IActivityTag)
    adapts(IDexterityContent)

    _delegated_attributes = [
        'related_activities',
    ]

    def __init__(self, context):
        self.context = aq_base(context)

    def __getattr__(self, key):
        if key in self._delegated_attributes:
            return getattr(self.context, key)
        raise AttributeError(key)

    def __setattr__(self, key, value):
        if key in self._delegated_attributes:
            setattr(self.context, key, value)
        self.__dict__[key] = value

    def __delattr__(self, key):
        if key in self._delegated_attributes:
            delattr(self.context, key)
        del self.__dict__[key]

