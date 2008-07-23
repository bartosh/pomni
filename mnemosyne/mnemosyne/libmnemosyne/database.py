##############################################################################
#
# database.py <Peter.Bienstman@UGent.be>
#
##############################################################################

from plugin import Plugin
from category import Category



##############################################################################
#
# Database
#
#  TODO: see if we need to break up this code
#
#  TODO: load_failed mechanism, to prevent overwriting a database which
#  failed to load.
#
##############################################################################

class Database(Plugin):
    
    ##########################################################################
    #
    # __init__
    #
    ##########################################################################
    
    def __init__(self, widget,
                 name, description, can_be_unregistered=True):

        self.type                = "batabase"
        self.name                = name
        self.description         = description
        self.can_be_unregistered = can_be_unregistered


        
    ##########################################################################
    #
    # Functions to be implemented by the actual database.
    #
    ##########################################################################
    
    # Creating, loading and saving the entire database.

    def new(self, path):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError
    
    def backup(self):
        raise NotImplementedError
    
    def load(self):
        raise NotImplementedError

    def is_loaded():
        raise NotImplementedError        

    # Start date.

    def save_start_date(self):
        raise NotImplementedError

    def load_start_date(self):
        raise NotImplementedError

    # Adding, modifying and deleting categories, facts and cards.

    # TODO: join add and modify into save?
    
    def add_category(self, category):
        raise NotImplementedError

    def modify_category(self, id, modified_category):
        raise NotImplementedError
    
    def delete_category(self, category):
        raise NotImplementedError

    def get_or_create_category_with_name(self, name):
        raise NotImplementedError        
    
    def remove_category_if_unused(self, cat):
        raise NotImplementedError        
    
    def add_fact(self, fact):
        raise NotImplementedError

    def modify_fact(self, id, modified_fact):
        raise NotImplementedError
    
    def delete_fact(self, fact):
        raise NotImplementedError
    
    def add_card(self, card): # should also link fact to new card
        raise NotImplementedError

    def modify_card(self, id, modified_card):
        raise NotImplementedError
    
    def delete_card(self, id, card):
        raise NotImplementedError
    
    # Queries. TODO: check which ones we need more.

    def category_names(self):
        raise NotImplementedError       
    
    def fact(self, id):
        raise NotImplementedError
    
    def card(self, id):
        raise NotImplementedError        

    def fact_count(self):
        raise NotImplementedError

    def card_count(self):
        raise NotImplementedError

    def non_memorised_count(self):
        raise NotImplementedError
    
    def scheduled_count(self):
        raise NotImplementedError

    def active_count(self):
        raise NotImplementedError
    
    def average_easiness(self):
        raise NotImplementedError        
    
    def cards_due_for_acq_rep(self):
        raise NotImplementedError
