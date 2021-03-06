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
Hildon UI. Common widgets (used in different modes).
"""

import gtk
import mnemosyne.maemo_ui.widgets.common as widgets

def create_gtkhtml(content=None):
    """ Create gtkhtml2 widget """

    def request_url(document, url, stream):
        """Get content from url."""
        uri = urlparse.urljoin("", url)
        fpurl = urllib.FancyURLopener().open(uri)
        stream.write(fpurl.read())
        fpurl.close()
        stream.close()

    def load_html(document, content):
        document.clear()
        document.open_stream("text/html")
        document.write_stream(content)
        document.close_stream()

    def link_clicked(object, url, document, view):
        """Called when link is clicked."""
        if url.startswith("#"):
            # jump to the local url(anchor)
            view.jump_to_anchor(url[1:])
            view.show()
        # open local html
        elif url.startswith("/"):
            load_html(document, open(url).read())
        else:
            # open browser here
            import webbrowser
            webbrowser.open(url)

            # start maemo browser via d-bus
            #import dbus
            #try:
            #    proxy_obj = dbus.SessionBus().get_object(\
            #        'com.nokia.osso_browser', '/com/nokia/osso_browser')
            #    dbus.Interface(proxy_obj,
            #        'com.nokia.osso_browser').load_url(url)
            #except dbus.exceptions.DBusException:
            #    import webbrowser
            #    webbrowser.open(url)

            # open url in the current view
            #urlfd = urllib2.urlopen(link)
            #content = urlfd.read()
            #urlfd.close()
            #load_html(document, content)

    import gtkhtml2
    import urllib
    #import urllib2
    import urlparse

    view = gtkhtml2.View()
    document = gtkhtml2.Document()
    document.connect('request_url', request_url)
    document.connect('link_clicked', link_clicked, document, view)
    if content:
        load_html(document, content)
    view.set_document(document)
    view.document = document
    view.show()
    return view

def create_tag_checkbox(name, active):
    """Create Tag item - GtkHBox with gtk.ToggleButton and gtk.Label."""

    hbox = gtk.HBox(homogeneous=False, spacing=10)
    button = gtk.ToggleButton()
    button.set_size_request(64, 64)
    button.set_active(active)
    button.set_name("tag_indicator")
    label = gtk.Label(name)
    label.set_name("black_label")
    hbox.pack_start(button, False)
    hbox.pack_start(label, False)
    hbox.show_all()
    return hbox

def create_button(name, callback=None, event='clicked', width=80, height=80):
    """Creates gtkButton widget."""

    button = gtk.Button()
    button.set_size_request(width, height)
    button.set_name(name)
    if callback is not None:
        button.connect(event, callback)
    return button

def create_radio_button(group=None, name=None, callback=None, \
     event='released', width=72, height=72):
    """Creates gtkRadioButton widget."""

    button = gtk.RadioButton(group)
    button.set_size_request(width, height)
    if name is not None:
        button.set_name(name)
    if callback is not None:
        button.connect(event, callback)
    return button

def create_toolbar_container(name, show_tabs=False, width=82, height=480):
    """Creates toolbar container."""

    container = gtk.Notebook()
    container.set_show_tabs(show_tabs)
    container.set_size_request(width, height)
    container.set_name(name)
    return container
