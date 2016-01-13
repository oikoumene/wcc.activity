from zope.interface import Interface

class IProductSpecific(Interface):
    pass

class IActivityTagEnabled(Interface):
    pass

class IActivityRelation(Interface):

    def related_news():
        pass

    def related_documents():
        pass
    
    def related_events():
        pass
    
