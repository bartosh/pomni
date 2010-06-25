#!/usr/bin/python -tt
# vim: sw=4 ts=4 expandtab ai
#
# Mnemosyne. Learning tool based on spaced repetition technique
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
Hildon UI. Widgets for input mode.
"""

import os
import gtk
import mnemosyne.maemo_ui.widgets.common as widgets
from mnemosyne.maemo_ui.widgets.common import create_tag_checkbox


def create_input_ui(main_switcher, theme_path):
    """Creates InputWidget UI."""

    def create_text_block(name):
        """Creates text field and text field container."""
        container = gtk.Frame()
        container.set_name('html_container')
        text_widget = gtk.TextView()
        text_widget.set_name(name)
        text_widget.set_justification(gtk.JUSTIFY_CENTER)
        text_widget.set_wrap_mode(gtk.WRAP_CHAR)
        return container, text_widget

    toplevel_table = gtk.Table(rows=1, columns=3)
    # create containers
    toolbar_container = widgets.create_toolbar_container('toolbar_container')
    toolbar_table = gtk.Table(rows=5, columns=1, homogeneous=True)
    grades_container = widgets.create_toolbar_container('grades_container')
    grades_table = gtk.Table(rows=6, columns=1, homogeneous=True)
    # create toolbar buttons
    card_type_button = widgets.create_button('undefined')
    content_button = widgets.create_button('undefined')
    tags_button = widgets.create_button('tags_button')
    menu_button = widgets.create_button('main_menu_button')
    # create sound button
    sound_container = gtk.Frame()
    sound_container.set_name('html_container')
    html = '<html><body><table align="center"><tr><td><img src=%s></td></tr>' \
        '</table></body></html>' % os.path.join(theme_path, "note.png")
    sound_button = widgets.create_gtkhtml(html)
    sound_container.add(sound_button)
    sound_box = gtk.VBox()
    sound_box.set_homogeneous(True)
    # create grades buttons
    grades = {}
    for num in range(6):
        grades[num] = widgets.create_button('grade%s' % num)
    # create text fields
    question_container, question_text = create_text_block('question_text')
    answer_container, answer_text = create_text_block('answer_text')
    foreign_container, foreign_text = create_text_block('foreign_text')
    pronunciation_container, pronunciation_text = create_text_block('pronunciation_text')
    translation_container, translation_text = create_text_block('translation_text')
    cloze_container, cloze_text = create_text_block('cloze_text')
    # create new tag elements
    tags_label = gtk.Label()
    tags_label.set_name('tags_label')
    tags_label.set_justify(gtk.JUSTIFY_LEFT)
    tags_label.set_single_line_mode(True)
    tags_layout = gtk.VBox(spacing=26)
    new_tag_box = gtk.HBox()
    new_tag_label = gtk.Label()
    new_tag_label.set_text('New tag: ')
    new_tag_label.set_name('white_label')
    new_tag_button = widgets.create_button('plus_button', width=60, height=60)
    new_tag_frame = gtk.Frame()
    new_tag_frame.set_name('html_container')
    new_tag_entry = gtk.Entry()
    new_tag_entry.set_name('entry_widget')
    # creates 'tags list' elements
    tags_frame = gtk.Frame()
    tags_frame.set_name('html_container')
    tags_eventbox = gtk.EventBox()
    tags_eventbox.set_visible_window(True)
    tags_eventbox.set_name('viewport_widget')
    tags_scrolledwindow = gtk.ScrolledWindow()
    tags_scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, \
        gtk.POLICY_AUTOMATIC)
    tags_scrolledwindow.set_name('scrolled_window')
    tags_viewport = gtk.Viewport()
    tags_viewport.set_name('viewport_widget')
    tags_viewport.set_shadow_type(gtk.SHADOW_NONE)
    tags_box = gtk.VBox()
    tags_box.set_homogeneous(True)
    # create other widgets
    two_sided_box = gtk.VBox(spacing=10)
    two_sided_box.set_homogeneous(True)
    three_sided_box = gtk.VBox(spacing=10)
    three_sided_box.set_homogeneous(True)
    cloze_box = gtk.VBox()
    widgets_table = gtk.Table(rows=2, columns=1)
    widgets_table.set_row_spacings(14)
    card_type_switcher = gtk.Notebook()
    card_type_switcher.set_show_tabs(False)
    card_type_switcher.set_show_border(False)
    # packing widgets
    toolbar_table.attach(card_type_button, 0, 1, 0, 1, \
        xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toolbar_table.attach(content_button, 0, 1, 1, 2, \
        xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toolbar_table.attach(tags_button, 0, 1, 2, 3, \
        xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toolbar_table.attach(menu_button, 0, 1, 4, 5, \
        xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    toolbar_container.add(toolbar_table)
    # packing grades buttons
    for pos in grades.keys():
        grades_table.attach(grades[pos], 0, 1, 5 - pos, 6 - pos, \
            xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
    grades_container.add(grades_table)
    # packing other widgets
    toplevel_table.attach(toolbar_container, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    toplevel_table.attach(grades_container, 3, 4, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL)
    widgets_table.attach(tags_label, 0, 1, 0, 1, \
        xoptions=gtk.SHRINK, yoptions=gtk.FILL, xpadding=4)
    widgets_table.attach(card_type_switcher, 0, 1, 1, 2, \
        xoptions=gtk.SHRINK|gtk.FILL|gtk.EXPAND, \
        yoptions=gtk.SHRINK|gtk.FILL|gtk.EXPAND)
    card_type_switcher.append_page(two_sided_box)
    card_type_switcher.append_page(three_sided_box)
    card_type_switcher.append_page(cloze_box)
    card_type_switcher.append_page(tags_layout)
    question_container.add(question_text)
    sound_box.pack_start(sound_container)
    sound_box.pack_end(question_container)
    answer_container.add(answer_text)
    two_sided_box.pack_start(sound_box)
    two_sided_box.pack_end(answer_container)
    foreign_container.add(foreign_text)
    pronunciation_container.add(pronunciation_text)
    translation_container.add(translation_text)
    three_sided_box.pack_start(foreign_container)
    three_sided_box.pack_start(pronunciation_container)
    three_sided_box.pack_end(translation_container)
    cloze_container.add(cloze_text)
    cloze_box.pack_start(cloze_container)
    new_tag_frame.add(new_tag_entry)
    new_tag_box.pack_start(new_tag_label, expand=False, fill=False, padding=10)
    new_tag_box.pack_start(new_tag_frame, expand=True, fill=True, padding=10)
    new_tag_box.pack_end(new_tag_button, expand=False, fill=False)
    tags_viewport.add(tags_box)
    tags_scrolledwindow.add(tags_viewport)
    tags_eventbox.add(tags_scrolledwindow)
    tags_frame.add(tags_eventbox)
    tags_layout.pack_start(new_tag_box, expand=False, fill=False)
    tags_layout.pack_end(tags_frame, expand=True, fill=True)
    toplevel_table.attach(widgets_table, 1, 2, 0, 1, \
        xoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, xpadding=30, \
        yoptions=gtk.SHRINK|gtk.EXPAND|gtk.FILL, ypadding=30)
    toplevel_table.show_all()
    # hide necessary widgets
    sound_container.hide()
    return main_switcher.append_page(toplevel_table), card_type_button, \
        content_button, menu_button, tags_button, sound_button, question_text, \
        answer_text, foreign_text, pronunciation_text, translation_text, \
        cloze_text, new_tag_button, new_tag_entry, tags_box, \
        card_type_switcher, sound_container, question_container, \
        toolbar_container, grades, tags_label, tags_button


def create_media_dialog_ui():
    """Creates MediaDialog UI."""

    def enable_select_button_cb(widget, select_button):
        """If user has select item - enable Select button."""
        select_button.set_sensitive(True)

    #liststore = [text, type, filename, dirname, pixbuf]
    liststore = gtk.ListStore(str, str, str, str, gtk.gdk.Pixbuf)
    dialog = gtk.Dialog()
    dialog.set_decorated(False)
    dialog.set_name('dialog')
    dialog.set_has_separator(False)
    dialog.resize(570, 410)
    width, height = dialog.get_size()
    dialog.move((gtk.gdk.screen_width() - width)/2, \
        (gtk.gdk.screen_height() - height)/2)
    iconview_widget = gtk.IconView()
    iconview_widget.set_name('iconview_widget')
    iconview_widget.set_model(liststore)
    iconview_widget.set_pixbuf_column(4)
    iconview_widget.set_text_column(0)
    label = gtk.Label('Select media')
    label.set_name('white_label')
    scrolledwindow_widget = gtk.ScrolledWindow()
    scrolledwindow_widget.set_policy(gtk.POLICY_NEVER, \
        gtk.POLICY_AUTOMATIC)
    scrolledwindow_widget.set_name('scrolledwindow_widget')
    scrolledwindow_widget.add(iconview_widget)
    widgets_table = gtk.Table(rows=1, columns=1)
    widgets_table.attach(scrolledwindow_widget, 0, 1, 0, 1, \
        xpadding=14, ypadding=14)
    dialog.vbox.pack_start(label, expand=False, fill=False, padding=4)
    dialog.vbox.pack_start(widgets_table)
    dialog.vbox.show_all()
    select_button = dialog.add_button('Select', gtk.RESPONSE_OK)
    select_button.set_size_request(262, 60)
    select_button.set_sensitive(False)            
    select_button.set_name('dialog_button')
    iconview_widget.connect('selection-changed', enable_select_button_cb, \
        select_button)
    cancel_button = dialog.add_button('Cancel', gtk.RESPONSE_REJECT)
    cancel_button.set_size_request(232, 60)
    cancel_button.set_name('dialog_button')
    dialog.action_area.set_layout(gtk.BUTTONBOX_SPREAD)
    dialog.action_area.set_homogeneous(True)
    return dialog, liststore, iconview_widget


def create_card_type_dialog_ui(selectors, front_to_back_id, both_ways_id, \
    three_sided_id, cloze_id, card_type_button, current_card_type, callback):
    """Creates CardType dialog UI."""
    
    from mnemosyne.maemo_ui.widgets.common import create_radio_button

    button = create_radio_button(None, 'front_to_back_cardtype_button', \
        callback)
    selectors[front_to_back_id]['selector'] = button
    button = create_radio_button(button, 'both_ways_cardtype_button', callback)
    selectors[both_ways_id]['selector'] = button
    button = create_radio_button(button, 'three_sided_cardtype_button', \
        callback)
    selectors[three_sided_id]['selector'] = button
    button = create_radio_button(button, 'cloze_cardtype_button', callback)
    selectors[cloze_id]['selector'] = button
    dialog = gtk.Dialog()
    dialog.set_decorated(False)
    dialog.set_name('dialog')
    dialog.set_has_separator(False)
    pos_x, pos_y = card_type_button.window.get_origin()
    dialog.move(pos_x, pos_y)
    buttons_table = gtk.Table(rows=1, columns=4, homogeneous=True)
    buttons_table.set_col_spacings(16)
    index = 0
    for selector in selectors.values():
        widget = selector['selector']
        if current_card_type is selector['card_type']:
            widget.set_active(True)
        buttons_table.attach(widget, index, index + 1, 0, 1, \
            xoptions=gtk.EXPAND, xpadding=6)
        index += 1
    dialog.vbox.pack_start(buttons_table, expand=True, fill=False, \
        padding=12)
    buttons_table.show_all()
    dialog.run()


def create_content_dialog_ui(callback, content_button, toolbar_container, \
    current_card_type, front_to_back_id):
    """Creates ContentDialog UI."""

    from mnemosyne.maemo_ui.widgets.common import create_button

    text_content_button = create_button('text_content_button', callback, \
        width=72, height=72)
    image_content_button = create_button('image_content_button', callback, \
        width=72, height=72)
    sound_content_button = create_button('sound_content_button', callback, \
        width=72, height=72)
    dialog = gtk.Dialog()
    dialog.set_decorated(False)
    dialog.set_name('dialog')
    dialog.set_has_separator(False)
    pos_x, pos_y = content_button.window.get_origin()
    dialog.move(pos_x, pos_y + toolbar_container.get_size_request()[1]/5)
    state = current_card_type.id in (front_to_back_id)
    sound_content_button.set_sensitive(state)
    image_content_button.set_sensitive(state)
    buttons_table = gtk.Table(rows=1, columns=3, homogeneous=True)
    buttons_table.set_col_spacings(16)
    buttons_table.attach(text_content_button, 0, 1, 0, 1, \
        xoptions=gtk.EXPAND, xpadding=10)
    buttons_table.attach(sound_content_button, 1, 2, 0, 1, \
        xoptions=gtk.EXPAND, xpadding=10)
    buttons_table.attach(image_content_button, 2, 3, 0, 1, \
        xoptions=gtk.EXPAND, xpadding=10)
    buttons_table.show_all()
    dialog.vbox.pack_start(buttons_table, expand=True, fill=False, \
        padding=8)
    dialog.run()


