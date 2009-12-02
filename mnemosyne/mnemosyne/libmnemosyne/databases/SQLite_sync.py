#
# SQLite_sync.py - Max Usachev <maxusachev@gmail.com>
#                  Ed Bartosh <bartosh@gmail.com>
#                  Peter Bienstman <Peter.Bienstman@UGent.be>
#

from openSM2sync.log_entry import LogEntry
from openSM2sync.log_entry import EventTypes

from mnemosyne.libmnemosyne.tag import Tag
from mnemosyne.libmnemosyne.fact import Fact
from mnemosyne.libmnemosyne.card import Card
from mnemosyne.libmnemosyne.card_type import CardType
from mnemosyne.libmnemosyne.fact_view import FactView


class SQLiteSync(object):

    """Code to be injected into the SQLite database class through inheritance,
    so that SQLite.py does not becomes too large.

    """
    
    def create_partnership_if_needed_for(self, partner):
        sql_res = self.con.execute("""select partner from partnerships 
           where partner=?""", (partner, )).fetchone()
        if not sql_res:
            self.con.execute("""insert into partnerships(partner, 
               _last_log_id) values(?,?)""", (partner, 0))

    def get_last_synced_log_entry_for(self, partner):
        sql_res = self.con.execute("""select _last_log_id from partnerships 
           where partner=?""", (partner, )).fetchone()
        return sql_res["_last_log_id"]
    
    def number_of_log_entries_to_sync_for(self, partner):
        _id = self.get_last_synced_log_entry_for(partner)
        return self.con.execute("select count() from log where _id>?",
            (_id, )).fetchone()[0]

    def _log_entry(self, sql_res):

        """Create log entry object in the format openSM2sync expects."""

        log_entry = LogEntry()
        log_entry["type"] = sql_res["event_type"]
        log_entry["time"] = sql_res["timestamp"]
        o_id = sql_res["object_id"]
        if o_id:
            log_entry["o_id"] = o_id        
        event_type = log_entry["type"]
        if event_type in (EventTypes.LOADED_DATABASE,
           EventTypes.SAVED_DATABASE):
            log_entry["sch"] = sql_res["acq_reps"]
            log_entry["n_mem"] = sql_res["ret_reps"]
            log_entry["act"] = sql_res["lapses"]            
        elif event_type in (EventTypes.ADDED_TAG, EventTypes.UPDATED_TAG):
            try:
                tag = self.get_tag(log_entry["o_id"], id_is_internal=False)
                log_entry["name"] = tag.name
                if tag.extra_data:
                    log_entry["extra"] = repr(tag.extra_data)
            except TypeError: # The object has been deleted at a later stage.
                pass
        elif event_type in (EventTypes.ADDED_FACT, EventTypes.UPDATED_FACT):
            try:
                fact = self.get_fact(log_entry["o_id"], id_is_internal=False)
                log_entry["c_time"] = fact.creation_time
                log_entry["m_time"] = fact.modification_time
                log_entry["card_t"] = fact.card_type.id
                for key, value in fact.data.iteritems():
                    log_entry[key] = value
            except TypeError: # The object has been deleted at a later stage.
                pass
        elif event_type == EventTypes.REPETITION:
            for attr in ("grade", "easiness", "acq_reps", "ret_reps", "lapses",
                "acq_reps_since_lapse", "ret_reps_since_lapse",
                "scheduled_interval", "actual_interval", "new_interval",
                "thinking_time"):
                log_entry[attr] = sql_res[attr]
        return log_entry
    
    def get_log_entries_to_sync_for(self, partner):

        """Note that we return an iterator here to be able to stream
        efficiently.

        """
        
        _id = self.get_last_synced_log_entry_for(partner)
        return (self._log_entry(cursor) for cursor in self.con.execute(\
            "select * from log where _id>?", (_id, )))

    def tag_from_log_entry(self, log_entry):
        # When deleting, the log entry only contains the tag's id, so we pull
        # the object from the database. This is a bit slower than just filling
        # in harmless missing fields, but it is more robust against future
        # side effects of tag deletion.
        if log_entry["type"] == EventTypes.DELETED_TAG:
            return self.get_tag(log_entry["o_id"], id_is_internal=False)
        # If we are creating a tag that will be deleted at a later stage
        # during the sync, we are missing some (irrelevant) information
        # needed to properly create a tag object.
        if "name" not in log_entry:
            log_entry["name"] = "irrelevant"
        tag = Tag(log_entry["name"], log_entry["o_id"])
        if "extra" in log_entry:
            tag.extra_data = eval(log_entry["extra"])
        # Make sure to create _id fields as well, otherwise database
        # operations or their side effects could fail.
        if log_entry["type"] != EventTypes.ADDED_TAG:
            tag._id = self.con.execute("select _id from tags where id=?",
                (tag.id, )).fetchone()[0]
        return tag
    
    def fact_from_log_entry(self, log_entry):
        if log_entry["type"] == EventTypes.DELETED_FACT:
            return self.get_fact(log_entry["o_id"], id_is_internal=False)
        if "card_t" not in log_entry:
            log_entry["card_t"] = "1"
            log_entry["c_time"] = "-1"
            log_entry["m_time"] = "-1"
        data = {}
        for key, value in log_entry.iteritems():
            if key not in ["time", "type", "o_id", "c_time", "m_time",
                "card_t"]:
                data[key] = value
        card_type = self.card_type_by_id(log_entry["card_t"])
        fact = Fact(data, card_type, log_entry["c_time"], log_entry["o_id"])
        fact.modification_time = log_entry["m_time"]
        if log_entry["type"] != EventTypes.ADDED_FACT:
            fact._id = self.con.execute("select _id from facts where id=?",
                (fact.id, )).fetchone()[0]
        return fact

    def apply_log_entry(self, log_entry):
        event_type = log_entry["type"]
        if event_type in (EventTypes.STARTED_PROGRAM,
           EventTypes.STOPPED_PROGRAM, EventTypes.STARTED_SCHEDULER):
            self.con.execute("""insert into log(event_type, timestamp,
               object_id) values(?,?,?)""", (event_type, log_entry["time"],
               log_entry["o_id"]))
        elif event_type in (EventTypes.LOADED_DATABASE,
           EventTypes.SAVED_DATABASE):
            self.con.execute("""insert into log(event_type, timestamp,
            acq_reps, ret_reps, lapses) values(?,?,?,?,?)""", (event_type,
            log_entry["time"], log_entry["sch"], log_entry["n_mem"],
            log_entry["act"]))
        elif event_type == EventTypes.ADDED_TAG:
            tag = self.tag_from_log_entry(log_entry)
            self.add_tag(tag, log_entry["time"])
        elif event_type == EventTypes.UPDATED_TAG:
            tag = self.tag_from_log_entry(log_entry)
            self.update_tag(tag, log_entry["time"])
        elif event_type == EventTypes.DELETED_TAG:
            tag = self.tag_from_log_entry(log_entry)
            self.delete_tag(tag, log_entry["time"])
        elif event_type == EventTypes.ADDED_FACT:
            fact = self.fact_from_log_entry(log_entry)
            self.add_fact(fact, log_entry["time"])
        elif event_type == EventTypes.UPDATED_FACT:
            fact = self.fact_from_log_entry(log_entry)
            self.update_fact(fact, log_entry["time"])
        elif event_type == EventTypes.DELETED_FACT:
            fact = self.fact_from_log_entry(log_entry)
            self.delete_fact_and_related_data(fact,log_entry["time"])
            
    def get_last_log_entry_index(self):
        return self.con.execute(\
            "select _id from log order by _id desc limit 1").fetchone()[0]
    
    def update_last_sync_log_entry_for(self, partner):
        self.con.execute(\
            "update partnerships set _last_log_id=? where partner=?",
            (self.get_last_log_entry_index(), partner))
