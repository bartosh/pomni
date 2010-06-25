#!/usr/bin/python -tt
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
Hildon UI: Input mode Widgets.
"""

import os
import gtk
import pango
import gettext

from mnemosyne.libmnemosyne.ui_components.dialogs import \
    AddCardsDialog, EditFactDialog
import mnemosyne.maemo_ui.widgets.input as widgets
import mnemosyne.maemo_ui.widgets.dialogs as dialogs
from mnemosyne.libmnemosyne.ui_component import UiComponent
from mnemosyne.libmnemosyne.utils import numeric_string_cmp
from mnemosyne.libmnemosyne.card_types.front_to_back import FrontToBack
from mnemosyne.libmnemosyne.card_types.both_ways import BothWays
from mnemosyne.libmnemosyne.card_types.three_sided import ThreeSided
from mnemosyne.libmnemosyne.card_types.cloze import Cloze
Cloze.required_fields = ["text"]

_ = gettext.gettext

FONT_DISTINCTION = 7

class InputWidget(UiComponent):
    """Input mode widget for Rainbow theme."""
    
    def __init__(self, component_manager):
        UiComponent.__init__(self, component_manager)
        self.conf = self.config()
        self.renderer = self.component_manager.get_current('renderer')
        self.default_tag_name = unicode(_("<default>"))
        self.content_type = None
        self.last_input_page = None
        self.fact = None
        self.sounddir = None
        self.imagedir = None
        self.card_type = None
        self.selected_tags = None
        self.tags = [unicode(tag) for tag in sorted( \
            self.database().get_tag_names(), cmp=numeric_string_cmp) or \
            [self.default_tag_name]]
        self._main_widget = self.main_widget()
        # create widgets
        self.window, card_type_button, content_type_button, tags_button, \
            question_text, answer_text, foreign_text, pronunciation_text, \
            translation_text, cloze_text, new_tag_button, card_type_switcher, \
            media_button, media_container, self.grades, tags_button = \
                widgets.create_input_ui(self.conf["theme_path"])
        # connect signals
        self.window.connect('destroy', self.input_to_main_menu_cb)
        content_type_button.connect('clicked', self.show_content_dialog_cb)
        tags_button.connect('clicked', self.show_tags_dialog_cb)
        #question_text.connect('button_release_event', self.show_media_dialog_cb)
        media_button.connect('button_press_event', self.show_media_dialog_cb)
        new_tag_button.connect('clicked', self.add_new_tag_cb)

        # create language switcher and set its callbacks for all text widgets
        langswitcher = self.component_manager.get_current("langswitcher")
        for widget in [question_text, answer_text, foreign_text, \
            pronunciation_text, translation_text, cloze_text]:
            widget.connect('focus-in-event', langswitcher.restore_cb)
            widget.connect('focus-out-event', langswitcher.save_cb)

        # widgets as attributes
        self.areas = {"cloze": cloze_text, "answer":  answer_text,
            "foreign": foreign_text, "pronunciation": pronunciation_text,
            "translation": translation_text, "question": question_text}

        # change default font
        font = pango.FontDescription("Nokia Sans %s" % \
            (self.conf['font_size'] - FONT_DISTINCTION))
        for area in self.areas.values():
            area.modify_font(font)

        self.widgets = {# Other widgets
            'CardTypeButton': card_type_button,
            'ContentTypeButton': content_type_button,
            'TagsButton': tags_button,
            'CardTypeSwitcher': card_type_switcher,
            'MediaButton': media_button,
            'MediaContainer': media_container,
            'QuestionText': question_text}

        # card_id: {"page": page_id, "card_type": card_type, 
        # "widgets": [(field_name:text_area_widget)...]}
        self.selectors = {
            FrontToBack.id: {
                "page": 0, 
                "widgets": [('q', question_text), ('a', answer_text)]},
            BothWays.id: {
                "page": 0,
                "widgets": [('q', question_text), ('a', answer_text)]},
            ThreeSided.id: {
                "page": 1,
                "widgets": [('f', foreign_text), ('t', translation_text),
                    ('p', pronunciation_text)]},
            Cloze.id: {
                "page": 2,
                "widgets": [('text', self.areas["cloze"])]}
        }

        # add card_type to selectors subdict
        for card_type in self.card_types():
            self.selectors[card_type.id]["card_type"] = card_type

        # turn off hildon autocapitalization
        try:
            for widget in self.areas.values():
                widget.set_property("hildon-input-mode", 'full')
        # stock gtk doesn't have hildon properties
        except (TypeError, AttributeError): 
            pass # so, skip silently

    def show_media_button(self, content_type='text'):
        """Shows of hides Media button."""

        if content_type in ('image', 'sound'):
            self.widgets['QuestionText'].hide()
            self.widgets['MediaContainer'].show()
            widgets.change_media_button_image(self.widgets['MediaButton'], \
                content_type, self.renderer, folder_mode=True)
        else:
            self.widgets['QuestionText'].show()
            self.widgets['MediaContainer'].hide()

    def set_card_type(self, card_type):
        """Set current Card type value and changes UI."""

        self.card_type = card_type
        widgets.change_cardtype_button_image( \
            self.widgets['CardTypeButton'], card_type, self.conf)
       
        self.widgets['CardTypeSwitcher'].set_current_page( \
            self.selectors[card_type.id]['page'])

        if card_type.id == FrontToBack.id:
            self.widgets['ContentTypeButton'].set_sensitive(True)
        else:
            self.widgets['ContentTypeButton'].set_sensitive(False)
            self.set_content_type('text')
            
    def set_content_type(self, content_type):
        """Set current Content type and changes UI."""

        self.content_type = content_type
        widgets.change_content_button_image(self.widgets['ContentTypeButton'], \
            content_type)
        self.show_media_button(content_type)

    def update_tags(self):
        """Update active tags list."""

        tags = ', '.join([tag.strip() for tag in self.selected_tags \
            if tag.strip() in self.tags]) or self.default_tag_name
        self.window.set_title(_('Tags: ') + tags)

    def check_complete_input(self):
        """Check for non empty fields."""

        pattern_list = ["<%s>" % caption.upper() for caption in self.areas]
        pattern_list.append("")
        for selector in self.selectors[self.card_type.id]["widgets"]:
            buf = selector[1].get_buffer()
            start, end = buf.get_bounds()
            if buf.get_text(start, end) in pattern_list:
                return False
        return True

    def get_widgets_data(self, check_for_required=True):
        """Get data from widgets."""

        fact = {}
        for fact_key, widget in self.selectors[self.card_type.id]["widgets"]:
            fact[fact_key] = unicode(self.get_textview_text(widget))
        if check_for_required:
            for required in self.card_type.required_fields:
                if not fact[required]:
                    raise ValueError
        return fact

    def set_widgets_data(self, fact):
        """Set widgets data from fact."""

        for fact_key, widget in self.selectors[self.card_type.id]['widgets']:
            widget.get_buffer().set_text(fact[fact_key])
        if self.content_type == 'sound':
            widgets.change_media_button_image(self.widgets['MediaButton'], \
                self.content_type, self.renderer, folder_mode=False)
        elif self.content_type == 'image':
            widgets.change_media_button_image(self.widgets['MediaButton'], \
                self.content_type, self.renderer, folder_mode=False, \
                fname=fact['q'], fname_is_html=True)

    def clear_widgets(self):
        """Clear widgets data."""

        for caption in self.areas:
            self.areas[caption].get_buffer().set_text("<%s>" % caption.upper())
        if self.content_type in ('image', 'sound'):
            widgets.change_media_button_image(self.widgets['MediaButton'], \
                self.content_type, self.renderer, folder_mode=True)

    def get_textview_text(self, widget):
        """Returns current text in textview."""

        start, end = widget.get_buffer().get_bounds()
        return widget.get_buffer().get_text(start, end)


    # Callbacks

    def show_tags_dialog_cb(self, widget):
        """Show TagsSelectionDialog."""

        self.selected_tags = widgets.create_tags_dialog_ui( \
            self.window, self.tags, self.selected_tags)
        self.update_tags()

    def add_new_tag_cb(self, widget):
        """Create new tag."""

        tag = unicode(widgets.create_new_tag_dialog_ui())
        if tag and not tag in self.tags:
            self.selected_tags.append(tag)
            self.tags.append(tag)
            self.update_tags()

    def show_cardtype_dialog_cb(self, widget):
        """Open CardTypeDialog."""

        self._main_widget.soundplayer.stop()
        selected_cardtype = widgets.create_card_type_dialog_ui(\
            self.window, self.card_types(), self.card_type)
        if selected_cardtype is not self.card_type:
            self.set_card_type(selected_cardtype)
            self.show_media_button()
            self.clear_widgets()

    def show_content_dialog_cb(self, widget):
        """Open ContentDialog."""

        self._main_widget.soundplayer.stop()
        self.set_content_type(widgets.create_content_dialog_ui( \
            self.window, self.content_type))

    def show_media_dialog_cb(self, widget, event):
        """Open MediaDialog."""

        fname = widgets.show_media_dialog(self.window, self.conf, \
            self.content_type)
        if not fname:
            return
        renderer = self.component_manager.get_current('renderer')
        if self.content_type == 'image':
            # draw fname picture
            widgets.change_media_button_image(self.widgets['MediaButton'], \
                self.content_type, renderer, folder_mode=False, fname=fname)            
            self.areas['question'].get_buffer().set_text('<img src=%s>' % fname)
        else:
            # draw sound logo
            widgets.change_media_button_image(self.widgets['MediaButton'], \
                self.content_type, renderer, folder_mode=False)
            self.areas['question'].get_buffer().set_text('<snd src=%s>' % fname)

    def preview_sound_in_input_cb(self, widget, event):
        """Listen sound in input mode."""

        if self._main_widget.soundplayer.stopped():
            self._main_widget.soundplayer.play(self.get_textview_text( \
                self.areas["question"]), self)
        else:
            self._main_widget.soundplayer.stop()

    def input_to_main_menu_cb(self, widget):
        """Return to main menu."""

        pass



class AddCardsWidget(AddCardsDialog, InputWidget):
    """Add new card widget."""

    def __init__(self, component_manager):
        InputWidget.__init__(self, component_manager)
        # connect signals
        self.widgets['CardTypeButton'].connect('clicked', \
            self.show_cardtype_dialog_cb)
        for button in self.grades.values():
            button.connect('clicked', self.add_card_cb)
        for text_area in self.areas.values():
            text_area.connect('button_press_event', self.clear_text_cb)
        self.selected_tags = [unicode(tag.strip()) for tag in \
            self.conf['tags_of_last_added'] if tag in self.tags]
        if not self.selected_tags:
            self.selected_tags = [self.default_tag_name]

    def activate(self):
        """Activate input mode."""

        # this part is the first part of add_cards from default controller
        self.stopwatch().pause()

        self.set_content_type(self.conf['content_type_last_selected'])
        self.set_card_type( \
            self.selectors[self.conf['card_type_last_selected']]['card_type'])
        self.update_tags()
        self.clear_widgets()

    def clear_text_cb(self, widget, event):
        """Clear textview content."""

        if self.get_textview_text(widget) in ["<%s>" % caption.upper() \
            for caption in self.areas]:
            widget.get_buffer().set_text("")

    def add_card_cb(self, widget):
        """Add card to database."""

        # check for empty fields
        if not self.check_complete_input():
            return

        try:
            fact_data = self.get_widgets_data()
        except ValueError:
            return # Let the user try again to fill out the missing data.

        grade = int(widget.name[-1])
        if grade in (0, 1):
            grade = -1
        self.controller().create_new_cards(fact_data, self.card_type, grade, \
            [unicode(tag).strip() for tag in self.selected_tags], save=True)
        self._main_widget.soundplayer.stop()
        self.clear_widgets()

    def input_to_main_menu_cb(self, widget):
        """Return to main menu."""

        conf = self.conf
        conf['tags_of_last_added'] = self.selected_tags
        conf['card_type_last_selected'] = self.card_type.id
        conf['content_type_last_selected'] = self.content_type
        conf.save()

        # this part is called from add_card_cb, when card is added
        self.database().save()
        review_controller = self.review_controller()
        review_controller.reload_counters()
        if review_controller.card is None:
            review_controller.new_question()
        self.stopwatch().unpause()

        self._main_widget.soundplayer.stop()
        self._main_widget.menu_()



class EditFactWidget(EditFactDialog, InputWidget):
    """Edit current fact widget."""

    def __init__(self, component_manager):
        InputWidget.__init__(self, component_manager)
        self.fact = self.review_controller().card.fact
        self.selected_tags = [tag.name for tag in \
            self.database().cards_from_fact(self.fact)[0].tags]
        # set grade of the current card active
        for num in range(6):
            self.grades[num].set_sensitive(False)
        current_grade = self.review_controller().card.grade
        if current_grade == -1:
            current_grade = 0
        self.grades[current_grade].set_sensitive(True)
        # connect signals
        self.grades[current_grade].connect('clicked', self.update_card_cb)
        self.window.connect('destroy', self.input_to_main_menu_cb)

    def activate(self):
        """Activate Edit mode."""

        # this part is the first part of
        # edit_current_card from default controller
        self.stopwatch().pause()

        self.set_card_type(self.fact.card_type)
        if self.card_type.id is FrontToBack.id:
            if 'img src=' in self.fact.data['q']:
                content_type = 'image'
            elif 'sound src=' in self.fact.data['q']:
                content_type = 'sound'
            else:
                content_type = 'text'
        else:
            content_type = 'text'
        
        self.widgets['CardTypeButton'].set_sensitive(False)
        self.widgets['ContentTypeButton'].set_sensitive(False)
        self.set_content_type(content_type)
        self.set_widgets_data(self.fact)
        self.update_tags()

    def update_card_cb(self, widget):
        """Update card in the database."""

        try:
            fact_data = self.get_widgets_data()
        except ValueError:
            return # Let the user try again to fill out the missing data.

        review_controller = self.review_controller()
        new_tags = [unicode(tag.strip()) for tag in self.selected_tags]
        self.controller().update_related_cards(self.fact, fact_data,
          self.card_type, new_tags, None)

        # this part is the second part of 
        # edit_current_fact from default controller
        review_controller.reload_counters()
        review_controller.card = self.database().get_card(\
            review_controller.card._id, id_is_internal=True)    
        review_controller.update_dialog(redraw_all=True)
        self.stopwatch().unpause()

        self.input_to_main_menu_cb()

    def input_to_main_menu_cb(self, widget=None):
        """Return to Review mode."""

        self._main_widget.soundplayer.stop()
        self.window.destroy()
        self._main_widget.activate_mode('review')


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
