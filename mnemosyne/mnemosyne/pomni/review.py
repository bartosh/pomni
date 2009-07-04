#!/usr/bin/python -tt7
# vim: sw=4 ts=4 expandtab ai
#
# Pomni. Learning tool based on spaced repetition technique
#
# Copyright (C) 2008 Pomni Development Team <pomni@googlegroups.com>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA
#

"""
Hildon UI. Review widgets.
"""

import gettext

from mnemosyne.libmnemosyne.ui_components.review_widget import ReviewWidget

_ = gettext.gettext

class RainbowReviewWidget(ReviewWidget):
    """Rainbow theme: Review Widget."""

    def __init__(self, component_manager):
        ReviewWidget.__init__(self, component_manager)
        self.next_is_image_card = False #Image card indicator
        self.w_tree = self.main_widget().w_tree
        self.w_tree.signal_autoconnect( \
            dict([(sig, getattr(self, sig + "_cb")) \
                for sig in ["review_to_main_menu", "get_answer", "grade", 
                "delete_card", "edit_card", "preview_sound_in_review"]]))

    def activate(self, param=None):
        """Activate review widget."""

        self.ui_controller_review().new_question()

    def enable_edit_current_card(self, enabled):
        """Enable or disable 'edit card' button."""

        self.w_tree.get_widget("review_toolbar_edit_card_button"). \
            set_sensitive(enabled)
        
    def enable_delete_current_card(self, enabled):
        """Enable or disable 'delete card' button."""

        self.w_tree.get_widget("review_toolbar_delete_card_button"). \
            set_sensitive(enabled)
        
    def set_question(self, text):
        """Set question."""

        document = self.w_tree.get_widget("question_text").document
        document.clear()
        document.open_stream('text/html')
        document.write_stream(self.manage_containers(text))
        document.close_stream()

    def set_answer(self, text):
        """Set answer."""

        document = self.w_tree.get_widget('answer_text').document
        document.clear()
        document.open_stream('text/html')
        if text.startswith('<html>'):
            font_size = self.config()['font_size']
            text = text.replace('*{font-size:30px;}',
                             '*{font-size:%spx;}' % font_size)
        document.write_stream(text)
        document.close_stream()
        
    def clear_question(self): 
        """Clear question text."""

        document = self.w_tree.get_widget('question_text').document
        document.clear()
        document.open_stream('text/html')
        document.write_stream('<html><body> </body></html>')
        document.close_stream()
        
    def clear_answer(self):
        """Clear answer text."""

        document = self.w_tree.get_widget('answer_text').document
        document.clear()
        document.open_stream('text/html')
        document.write_stream('<html><body> </body></html>')
        document.close_stream()
        
    def update_show_button(self, text, default, enabled): 
        """Update show button."""

        self.w_tree.get_widget("answer_container").set_sensitive(enabled)
        if enabled:
            if self.next_is_image_card:
                html = "<html><p align=center style='margin-top:20px; \
                    font-size:20;'>%s</p></html>" % text
            else:
                html = "<html><p align=center style='margin-top:70px; \
                    font-size:20;'>%s</p></html>" % text
            document = self.w_tree.get_widget("answer_text").document
            document.clear()
            document.open_stream('text/html')
            document.write_stream(html)
            document.close_stream()

    def enable_grades(self, enabled):
        """Enable grades."""

        self.w_tree.get_widget("grades_table").set_sensitive(enabled)
        self.enable_edit_current_card(enabled)
        self.enable_delete_current_card(enabled)

    def manage_containers(self, text):
        """Shows or hides snd container."""

        self.next_is_image_card = "img src=" in text
        params = self.w_tree.get_widget("question_text").window.get_geometry()
        if "sound src=" in text:
            self.sndtext = text
            self.w_tree.get_widget("question_container").hide()
            self.w_tree.get_widget("review_mode_snd_container"). \
                set_size_request(params[2], 16)
            self.w_tree.get_widget("review_mode_snd_container").show()
            self.w_tree.get_widget("review_mode_snd_button").set_active(True)
            self.main_widget().start_playing(self.sndtext, self)
        elif "img src=" in text:
            self.w_tree.get_widget("review_mode_snd_container").hide()
            self.w_tree.get_widget("question_container"). \
                set_size_request(params[2], 260)
            self.w_tree.get_widget("question_container").show()
        else:
            self.w_tree.get_widget("review_mode_snd_container").hide()
            self.w_tree.get_widget("question_container"). \
                set_size_request(params[2], 16)
            self.w_tree.get_widget("question_container").show()
            if text.startswith('<html>'):
                font_size = self.config()['font_size']
                new_text = text.replace('*{font-size:30px;}',
                    '*{font-size:%spx;}' % font_size)
            return new_text
        return text

    def update_indicator(self):
        """Set non active state for widget."""

        self.w_tree.get_widget("review_mode_snd_button").set_active(False)

    # callbacks
    def preview_sound_in_review_cb(self, widget):
        """Play/stop listening."""

        if widget.get_active():
            self.main_widget().start_playing(self.sndtext, self)
        else:
            self.main_widget().stop_playing()

    def review_to_main_menu_cb(self, widget):
        """Return to main menu."""

        self.main_widget().stop_playing()
        self.main_widget().activate_mode("menu")

    def get_answer_cb(self, widget, event):
        """Hook for showing a right answer."""

        self.ui_controller_review().show_answer()

    def delete_card_cb(self, widget):
        """Hook for delete card."""

        self.main_widget().stop_playing()
        self.ui_controller_main().delete_current_fact()

    def edit_card_cb(self, widget):
        """Hook for edit card."""

        self.ui_controller_main().edit_current_card()

    def grade_cb(self, widget):
        """Call grade of answer."""

        self.main_widget().stop_playing()
        self.ui_controller_review().grade_answer(int(widget.name[-1]))

    def set_default_grade(self, grade):
        #print 'set_default_grade', grade
        pass
        
    def set_grades_title(self, text): 
        #print 'set_grades_title', text
        pass
            
    def set_grade_text(self, grade, text): 
        #print 'set_grade_text', text
        pass
            
    def set_grade_tooltip(self, grade, text): 
        #print 'set_grade_tooltip', grade, text
        pass

    def update_status_bar(self, message=None):
        #print 'update_status_bar', message
        pass

    def enable_edit_deck(self, enable): 
        #print 'enable_edit_deck', enable
        pass
        
    def question_box_visible(self, visible):
        #print 'question_box_visible', visible
        pass
        
    def answer_box_visible(self, visible):
        #print 'answer_box_visible', visible
        pass
        
    def set_question_label(self, text):
        #print 'set_question_label', text
        pass




# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End: