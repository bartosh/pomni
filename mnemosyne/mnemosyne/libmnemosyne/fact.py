#
# fact.py <Peter.Bienstman@UGent.be>
#

import time

from mnemosyne.libmnemosyne.utils import CompareOnId


class Fact(CompareOnId):

    """Basic unit of information from which several cards can be derived.

    The fields are stored in a dictionary called 'data', and can be get and 
    set using the standard dictionary syntax.

    Creating and modification dates are POSIX timestamps stored as integers.

    'id' is used to identify this object to the external world (logs, xml
    files, ...), whereas '_id' is an internal id that could be different and
    that can be used by the database for efficiency reasons.

    The keys in data should be in the latin charset for the sake of the
    syncing procedure, but they can be given more descriptive names inside the
    CardType class.

    When making new card types, it is best to reuse the keys below as much
    as possible, to facilitate conversion between card types:

    === =============
     q  question
     a  answer
     f  foreign word
     t  translation
     p  pronunciation
    === =============

    """

    def __init__(self, data, card_type, creation_time=None, id=None):
        #print "Fact.py __init__ method"
        if creation_time is None:
            creation_time = int(time.time())
        self.creation_time = creation_time
        self.modification_time = self.creation_time
        self.data = data
        self.card_type = card_type
        if id is None:
            import uuid
            id = str(uuid.uuid4())
        self.id = id
        self._id = None
        #print "fact.data =", self.data
        #print "fact.card_type =", self.card_type
        #print "--- card type ---"
        #print "fact.card_type.firelds =", self.card_type.fields
        #print "fact.card_type.required_firelds =", self.card_type.required_fields()
        #print "fact.card_type.keys() =", self.card_type.keys()
        #print "fact.card_type.key_names() =", self.card_type.key_names()
        #print "--- card type ---"
        #print "fact.id =", self.id
        #print "fact._id =", self._id
        #print "fact.creation_time =", self.creation_time
        #print "fact.modification_time =", self.modification_time
        #print "fact.instance =", self

    def __eq__(self, other):
        try:
            return self.id == other.id
        except:
            return False
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __setitem__(self, key, value):
        self.data[key] = value
        
