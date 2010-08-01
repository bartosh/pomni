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
Converts old database to current db-format.
"""

from mnemosyne.libmnemosyne.databases.SQLite_logging \
    import SQLiteLogging as events


class DBFixer:
    def __init__(self, database, component_manager):
        self.database = database
        self.connection = database.con
        self.component_manager = component_manager

    def fix_indexes(self):
        """Checking indexes existence and creating if needed."""

        if self.connection.execute("""SELECT name FROM sqlite_master 
            WHERE name='i_log_object_id'""").fetchone() is None:
            self.connection.execute("""CREATE INDEX i_log_object_id ON 
                log (object_id)""")

        if self.connection.execute("""SELECT name FROM sqlite_master 
            WHERE name='i_log_timestamp'""").fetchone() is None:
            self.connection.execute("""CREATE INDEX i_log_timestamp ON 
                log (timestamp)""")
        self.connection.commit()

    def fix(self):
        """Checking existence of 'activity_criteria' table."""

        #Upgrade from python-libmnemosyne 2.0.0-14 to 2.0.0-15
        if self.connection.execute("""SELECT name FROM sqlite_master 
            WHERE name='activity_criteria'""").fetchone() is None:
            self.connection.execute("""CREATE TABLE activity_criteria 
                (_id integer primary key, id text, name text, type text, 
                    data text)""")
            self.connection.commit()

            from mnemosyne.libmnemosyne.activity_criteria.default_criterion \
                import DefaultCriterion
            criterion = DefaultCriterion(self.component_manager)
            self.database.add_activity_criterion(criterion)
            self.connection.commit()

            self.fix_indexes()
            self.fix_cards()

    def fix_cards(self):
        """Fixing cards in different tables."""

        # Fixing 'cards' table.
        for cursor in self.connection.execute( \
            """SELECT _id, id, fact_view_id from cards"""):
            new_fact_view_id = cursor['id'][-3:].replace('.', '::')
            new_id = cursor['id'][:-1] + new_fact_view_id
            self.connection.execute("""UPDATE cards SET id=?, fact_view_id=? 
                WHERE _id=?""", (new_id, new_fact_view_id, cursor['_id']))

        # Fixing 'log' table.
        card_events = (events.ADDED_CARD, events.UPDATED_CARD, \
            events.DELETED_CARD)
        for cursor in self.connection.execute( \
            """SELECT _id, event, object_id from log"""):
            if cursor['event'] in card_events:
                new_object_id = cursor['object_id'][:-1] + \
                    cursor['object_id'][-3:].replace('.', '::')
                self.connection.execute("""UPDATE log SET object_id=? 
                    WHERE _id=?""", (new_object_id, cursor['_id']))
        self.connection.commit()
