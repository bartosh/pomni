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
Hildon UI. Statistics widget.
"""

import time

from mnemosyne.libmnemosyne.ui_components.dialogs import StatisticsDialog
from mnemosyne.libmnemosyne.statistics_pages.current_card \
    import CurrentCardStatPage
from mnemosyne.maemo_ui.widgets.statistics import create_statistics_ui


class MaemoCurrentCard(CurrentCardStatPage):

    def __init__(self, component_manager):
        CurrentCardStatPage.__init__(self, component_manager)
        self.text = ""

    def prepare_statistics(self, variant):
        """ Preparing for Label widget """

        data = self.get_data()
        text = """<span  foreground='white' size="x-large">"""
        if data.has_key('error'):
            text += data['error']
        else:
            text += "Grade %d\n" % data["grade"]  
            text += "Easiness %1.2f\n" % data["easiness"]
            text += "Repetitions %d\n" % data["repetitions"]
            text += "Lapses %d\n" % data["lapses"]
            text += "Interval %d" % data["interval"]
            text += "Last repetition %s\n" \
                % time.strftime("%B %d, %Y", data["last_repetition"])
            text += "Next repetition %s\n" \
                % time.strftime("%B %d, %Y", data["next_repetition"])
            text += "Average thinking time (secs) %d\n" \
                % data["avg_thinking_time"]
            text += "Total thinking time (secs) %d\n" \
                % data["total_thinking_time"]
        text += "</span>"
        self.text = text
        return text

class MaemoStatisticsWidget(StatisticsDialog, MaemoCurrentCard):
    """Statistics Widget."""

    def __init__(self, component_manager, previous_mode=None):
        self.statistics_text = ""
        StatisticsDialog.__init__(self, component_manager)
        MaemoCurrentCard.__init__(self, component_manager)
        # create widgets
        self.page, menu_button = create_statistics_ui(\
            self.main_widget().switcher, self.prepare_statistics()) 
        # connect signals
        if previous_mode == 'Menu':
            menu_button.connect('clicked', self.back_to_main_menu_cb)
        else:
            menu_button.connect('clicked', self.back_to_previous_mode_cb)

    def activate(self):
        """Set necessary switcher page."""

        self.main_widget().switcher.set_current_page(self.page)

    def back_to_previous_mode_cb(self, widget):
        """Returns to previous menu."""

        self.main_widget().switcher.remove_page(self.page)

    def back_to_main_menu_cb(self, widget):
        """Returns to main menu."""

        self.main_widget().switcher.remove_page(self.page)
        self.main_widget().menu_('statistics')

