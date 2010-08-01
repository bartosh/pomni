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
    """Fix database when structure changed."""

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

        # Upgrade from python-libmnemosyne 2.0.0-16~rc2 to 2.0.0-17~rc1
        version = self.connection.execute("""select value from global_variables
                   where key=?""", ("version", )).fetchone()["value"]
        if version == "SQL 1.0":
            self.upgrade_from_16rc2_to_17rc1()


    def upgrade_from_16rc2_to_17rc1(self):
        """Upgrade from python-libmnemosyne 2.0.0-16~rc2 to 2.0.0-17~rc1
           from db version "SQL 1.0" to "Mnemosyne SQL 1.0".
        """

        if not self.connection.execute("""SELECT name FROM sqlite_master
          WHERE name='i_facts'""").fetchone():
            self.connection.execute("create index i_facts ON facts (id)")
        if not self.connection.execute("""SELECT name FROM sqlite_master
          WHERE name='i_cards'""").fetchone():
            self.connection.execute("create index i_cards ON cards (id)")
        if not self.connection.execute("""SELECT name FROM sqlite_master
          WHERE name='i_tags'""").fetchone():
            self.connection.execute("create index i_tags ON tags (id)")

        self.connection.executescript("""create table log_temp(
            _id integer primary key autoincrement,
            event_type integer,
            timestamp integer,
            object_id text,
            grade integer,
            easiness real,
            acq_reps integer,
            ret_reps integer,
            lapses integer,
            acq_reps_since_lapse integer,
            ret_reps_since_lapse integer,
            scheduled_interval integer,
            actual_interval integer,
            new_interval integer,
            thinking_time integer,
            last_rep integer,
            next_rep integer,
            scheduler_data integer
            );

           insert into log_temp(_id, event_type,
              timestamp, object_id, grade, easiness, acq_reps, ret_reps,
              lapses, acq_reps_since_lapse, ret_reps_since_lapse,
              scheduled_interval, actual_interval, new_interval, thinking_time)
              select * from log;

           drop index i_log_timestamp;
           drop index i_log_object_id;
           drop table log;
           alter table log_temp rename to log;
           create index i_log_timestamp on log (timestamp);
           create index i_log_object_id on log (object_id);

           create table media_temp(
                filename text primary key,
                _hash text
           );
           insert into media_temp(filename) select filename from media;
           drop table media;
           alter table media_temp rename to media;

           create table fact_views_for_card_type_temp(
                _fact_view_id integer,
                card_type_id text
           );

           insert into fact_views_for_card_type_temp select * from fact_views_for_card_type;
           drop table fact_views_for_card_type;
           alter table fact_views_for_card_type_temp
                       rename to fact_views_for_card_type;""")

        for cursor in self.connection.execute("select filename from media"):
            filename = cursor['filename']
            self.connection.execute("update media set _hash=? "
                                    "where filename=?", (filename,
                                    self.database._media_hash(filename)))

        self.connection.execute("""update global_variables
                            set value='Mnemosyne SQL 1.0'
                            where key='version' and value='SQL 1.0'""")

        self.connection.commit()

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
