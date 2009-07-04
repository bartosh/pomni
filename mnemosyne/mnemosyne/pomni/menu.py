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
Hildon UI. Menu widgets.
"""

from mnemosyne.libmnemosyne.ui_component import UiComponent

class RainbowMenuWidget(UiComponent):

    review, input, configuration = range(1, 4)

    def __init__(self, component_manager):
        UiComponent.__init__(self, component_manager)

        self.w_tree = self.main_widget().w_tree
        self.switcher = self.main_widget().switcher

        self.w_tree.signal_autoconnect(\
            dict([(mode, getattr(self, mode + "_cb")) \
                for mode in ["input", "review", "configure", "exit"]]))

    def activate(self, param=None):
        pass

    # callbacks
    def input_cb(self, widget):
        """Return to main menu."""
        self.main_widget().input_(widget)

    def review_cb(self, widget):
        self.main_widget().review_(widget)

    def configure_cb(self, widget):
        self.main_widget().configure_(widget)

    def exit_cb(self, widget):
        self.main_widget().exit_(widget)


############### old design #############################

class HildonUiControllerMain():
    """ Hidon Main Controller  """

    def show(self):
        """ Start base class """
        self.switcher.set_current_page(self.main_menu)

    def edit_current_card(self):
        """ Not Implemented Yet """

        pass

    def update_related_cards(self, fact, new_fact_data, new_card_type, \
                             new_cat_names):
        """ Not Implemented """

        pass


    def file_new(self):
        """ Not Implemented Yet """

        pass

    def file_open(self):
        """ Not Implemented Yet """

        pass

    def file_save(self):
        """ Not Implemented Yet """

        pass

    def file_save_as(self):
        """ Not Implemented Yet """

        pass



class EternalControllerMain(HildonUiControllerMain):
    """ Eternal UI Main Controller """

    def activate(self):
        self.w_tree.signal_autoconnect({"size_allocate": self.size_allocate_cb})
        self.spliter_trigger = True

    def size_allocate_cb(self, widget, user_data):
        """ Checking window size """

        if (self.switcher.get_current_page() == self.review):
            if (self.spliter_trigger):
                # Set Spliter (GtkVpan) to pseudo medium
                self.spliter_trigger = False
                pseudo_medium = (widget.allocation.height - 70)/2 - 20
                self.spliter.set_property('position', pseudo_medium)
            else:
                self.spliter_trigger = True

class RainbowControllerMain(HildonUiControllerMain):
    """ Rainbow UI Main Controller """

    def activate(self):
        pass


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End: