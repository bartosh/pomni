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
Hildon UI. Menu widget.
"""

import mnemosyne.maemo_ui.widgets.menu as widgets
#import create_menu_ui
from mnemosyne.libmnemosyne.ui_component import UiComponent

class MenuWidget(UiComponent):
    """Main menu widget."""

    component_type = "menu_widget"

    def __init__(self, component_manager, exit_callback):
        UiComponent.__init__(self, component_manager)
        self._main_widget = self.main_widget()
        # create widgets
        #self.page, buttons = widgets.create_menu_ui(self._main_widget.switcher)
        self.window, review_button = widgets.create_menu_ui(exit_callback)
        """
        # connect signals
        buttons['tags'].connect('clicked', self.tags_cb)
        buttons['review'].connect('clicked', self.review_cb)
        buttons['input'].connect('clicked', self.input_cb)
        buttons['settings'].connect('clicked', self.settings_cb)
        #buttons['sync'].connect('clicked', self.sync_cb)
        buttons['import'].connect('clicked', self.importcards_cb)
        buttons['stats'].connect('clicked', self.statistics_cb)
        buttons['help'].connect('clicked', self.about_cb)
        buttons['exit'].connect('clicked', self.exit_cb)
        """
        review_button.connect('clicked', self.review_cb)
        self._main_widget.window = self.window

    def activate(self):
        """Activates necessary switcher page."""

        #self._main_widget.switcher.set_current_page(self.page)
        #self.window.show_all()
        print self._main_widget.widgets

    # callbacks
    def tags_cb(self, widget):
        """Go to Tags mode."""

        self._main_widget.switcher.remove_page(self.page)
        self._main_widget.tags_()

    def input_cb(self, widget):
        """Go to Input mode."""

        self._main_widget.switcher.remove_page(self.page)
        self._main_widget.input_()

    def review_cb(self, widget):
        """Go to Review mode."""

        #self._main_widget.switcher.remove_page(self.page)
        self._main_widget.review_()

    def sync_cb(self, widget):
        """Go to Sync mode."""

        self._main_widget.switcher.remove_page(self.page)
        self._main_widget.sync_()

    def settings_cb(self, widget):
        """Go to Configuration mode."""

        self._main_widget.switcher.remove_page(self.page)
        self._main_widget.configure_()

    def statistics_cb(self, widget):
        """Go to Statistics mode."""

        self._main_widget.switcher.remove_page(self.page)
        self._main_widget.statistics_()

    def importcards_cb(self, widget):
        """Go to import mode."""

        self._main_widget.switcher.remove_page(self.page)
        self._main_widget.import_()

    def about_cb(self, widget):
        """Go to About mode."""

        self._main_widget.switcher.remove_page(self.page)
        self._main_widget.about_()

    def exit_cb(self, widget):
        """Exit program."""

        self._main_widget.exit_()


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
