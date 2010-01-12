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
Hildon UI. About Widget.
"""

import os
import mnemosyne.maemo_ui.widgets.about as widgets
from mnemosyne.libmnemosyne.ui_component import UiComponent


class AboutWidget(UiComponent):
    """About Widget."""

    def __init__(self, component_manager):
        UiComponent.__init__(self, component_manager, )
        # create widgets
        self.page, self.switcher, menu_button, about_button, help_button = \
            widgets.create_about_ui(self.main_widget().switcher,
                os.path.join(self.config()['theme_path'], "mnemosyne.png"),
                os.path.join(self.config()['html_path'], "help.html"))
        # connect signals
        menu_button.connect('clicked', self.about_to_main_menu_cb)
        about_button.connect('released', self.show_about_cb)
        help_button.connect('released', self.show_help_cb)
        if self.config()['last_about_page'] == 0:
            about_button.set_active(True)
            self.show_about_cb(None)
        else:
            help_button.set_active(True)
            self.show_help_cb(None)

    def activate(self):
        """Set necessary switcher page."""

        self.main_widget().switcher.set_current_page(self.page)

    def show_about_cb(self, widget):
        """Show program about information."""
        
        self.switcher.set_current_page(0)

    def show_help_cb(self, widget):
        """Show program documentation."""
        
        self.switcher.set_current_page(1)

    def about_to_main_menu_cb(self, widget):
        """Returns to main menu."""

        self.config()['last_about_page'] = self.switcher.get_current_page()
        self.config().save()
        self.main_widget().switcher.remove_page(self.page)
        self.main_widget().menu_('about')
       
