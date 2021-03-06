#
# dialogs.py <Peter.Bienstman@UGent.be>
#

from mnemosyne.libmnemosyne.ui_component import UiComponent


class Dialog(UiComponent):

    component_type = "dialog"
    instantiate = UiComponent.LATER


class AddCardsDialog(Dialog):
         
    component_type = "add_cards_dialog"


class EditFactDialog(Dialog):
    
    component_type = "edit_fact_dialog"

    def __init__(self, fact, component_manager, allow_cancel=True):
        pass


class ActivateCardsDialog(Dialog):
    
    component_type = "activate_cards_dialog"

    
class BrowseCardsDialog(Dialog):
    
    component_type = "browse_cards_dialog"


class CardAppearanceDialog(Dialog):
    
    component_type = "card_appearance_dialog"

    
class ActivatePluginsDialog(Dialog):
    
    component_type = "activate_plugins_dialog"


class ManageCardTypesDialog(Dialog):
    
    component_type = "manage_card_types_dialog"


class StatisticsDialog(Dialog):
    
    component_type = "statistics_dialog"


class ConfigurationDialog(Dialog):
    
    component_type = "configuration_dialog"


class ProgressDialog(Dialog):

    component_type = "progress_dialog"

    def set_range(self, minimum, maximum):
        pass

    def set_text(self, text):
        pass

    def set_value(self, value):
        pass
