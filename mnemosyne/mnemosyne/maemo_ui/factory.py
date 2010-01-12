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
UI Factory. Creates UI objects
"""

from mnemosyne.libmnemosyne import Mnemosyne
from mnemosyne.libmnemosyne.component import Component

class ConfigHook(Component):
    """Configuration hook."""
    component_type = 'hook'
    used_for = 'configuration_defaults'

    def run(self):
        """Entry point."""
        for key, value in {\
            "theme_path": "/usr/share/mnemosyne/hildon-UI/dark",
            "html_path": "/usr/share/mnemosyne/html",
            "fullscreen": True,
            "font_size": 30.0,
            "startup_with_review": False,
            "upload_logs": False,
            "imagedir": "/home/user/MyDocs/.images",
            "sounddir": "/home/user/MyDocs/.sounds",
            "last_settings_page": 0,
            "last_about_page": 0,
            "last_selected_grade": 1,
            "server_login": "mnemosyne",
            "server_passwd": "mnemosyne",
            "server_sync_port": "",
            "server_sync_address": "",
            "client_login": "mnemosyne",
            "client_passwd": "mnemosyne",
            "client_sync_port": "",
            "client_sync_address": "",
            "tts_language": "english",
            "tts_voice": "Male",
            "tts_speed": 100,
            "tts_pitch": 30,
            "card_type_last_selected": "1",
            "content_type_last_selected": "text",
            "times_loaded": 0}.iteritems():

            self.config().setdefault(key, value)

        self.config()["upload_logs"] = False

def app_factory(interface=None):
    """Mnemosyne application factory."""

    app = Mnemosyne()
    app.components.append(("mnemosyne.maemo_ui.factory", "ConfigHook"))

    if not interface or interface == "hildon":
        # Remove not used components
        app.components.remove(\
            ("mnemosyne.libmnemosyne.card_types.map", "MapPlugin"))
        app.components.remove(\
            ("mnemosyne.libmnemosyne.card_types.cloze", "ClozePlugin"))
        app.components.remove(\
            ("mnemosyne.libmnemosyne.plugins.cramming_plugin", \
            "CrammingPlugin"))
        app.components.remove(\
            ("mnemosyne.libmnemosyne.renderers.html_css", "HtmlCss"))
        app.components.remove(\
            ("mnemosyne.libmnemosyne.filters.escape_to_html", "EscapeToHtml"))
        app.components.remove(\
            ("mnemosyne.libmnemosyne.filters.expand_paths", "ExpandPaths"))
        app.components.remove(\
            ("mnemosyne.libmnemosyne.filters.latex", "Latex"))
        app.components.remove(\
            ("mnemosyne.libmnemosyne.filters.html5_media", "Html5Media"))

        # Add necessary components
        app.components.insert(0, ("mnemosyne.libmnemosyne.translator",
                                  "GetTextTranslator"))
        app.components.append(("mnemosyne.maemo_ui.renderers", "Html"))
        app.components.append(("mnemosyne.maemo_ui.main", "MainWdgt"))
        app.components.append(("mnemosyne.maemo_ui.menu", "MenuWidget"))
        app.components.append(("mnemosyne.maemo_ui.review", "ReviewWdgt"))
        app.components.append(("mnemosyne.maemo_ui.input", "AddCardsWidget"))
        app.components.append(("mnemosyne.maemo_ui.input", "EditFactWidget"))
        app.components.append(\
            ("mnemosyne.maemo_ui.configuration", "ConfigurationWidget"))
        #app.components.append(("mnemosyne.maemo_ui.sync", "SyncWidget"))
        app.components.append(("mnemosyne.maemo_ui.tags", "TagsWidget"))
        app.components.append(("mnemosyne.maemo_ui.statistics", "MaemoStatisticsWidget"))
        app.components.append(("mnemosyne.maemo_ui.importcards", "ImportCardsWidget"))
        app.components.append(("mnemosyne.libmnemosyne.file_formats.tsv", "TabSeparated"))

        app.components.append(\
            ("mnemosyne.libmnemosyne.card_types.cloze", "Cloze"))
        app.components.append(\
            ("mnemosyne.maemo_ui.langswitcher", "LangSwitcher"))
        return app

    # add next gui here
    raise ValueError("No idea how to create %s app" % interface)


# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
