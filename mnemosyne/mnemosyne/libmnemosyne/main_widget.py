#
# main_widget.py <Peter.Bienstman@UGent.be>
#

import gettext
_ = gettext.gettext


class MainWidget(object):
    
    """Describes the interface that the main widget needs to implement
    in order to be used by the main controller.

    """
    
    def after_mnemosyne_init(self):

        """If the widget needs to do some initialisation which requires
        libmnemosyne to be already initialised, this can go here.

        """
        
        pass
    
    def init_review_widget(self):

        """At the very least, this function has to inform the controller
        about its review widget.

        """
        
        pass
    
    def information_box(self, message, OK_string=_("&OK")):
        pass
            
    def question_box(self, question, option0, option1, option2):
        pass
    
    def error_box(self, message):
        pass

    def show_exception(self, exception):
        if exception.info:
            exception.msg += "\n" + exception.info
        self.error_box(exception.msg)
    
    def save_file_dialog(self, path, filter, caption=""):
        pass
    
    def open_file_dialog(self, path, filter, caption=""):
        pass
    
    def run_add_card_dialog(self):
        pass

    def run_edit_fact_dialog(self, fact, allow_cancel=True):
        pass
    
    def run_card_appearance_dialog(self):
        pass

    def run_manage_card_types_dialog(self):
        pass
    
    def update_status_bar(self, message=None):
        pass 
