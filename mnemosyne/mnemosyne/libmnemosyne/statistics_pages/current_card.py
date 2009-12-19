#
# current_card.py <Peter.Bienstman@UGent.be>
#

import time

from mnemosyne.libmnemosyne.translator import _
from mnemosyne.libmnemosyne.statistics_page import StatisticsPage

DAY = 24 * 60 * 60 # Seconds in a day.

class CurrentCardStatPage(StatisticsPage):

    """A statistics for current card."""

    def __init__(self, component_manager):
        StatisticsPage.__init__(self, component_manager)

    def get_data(self):
        """Get statistics data."""

        card = self.review_controller().card
        if not card:
            self._data["error"] = _("No current card.")
        elif card.grade == -1:
            self._data["error"] = _("Unseen card, no statistics available yet.")
        else:
            db = self.database()
            self._data["grade"] = card.grade 
            self._data["easiness"] = card.easiness 
            self._data["repetitions"] = (card.acq_reps + card.ret_reps)
            self._data["lapses"] = card.lapses
            self._data["interval"] = card.interval / DAY
            self._data["last_repetition"] =  time.gmtime(card.last_rep)
            self._data["next_repetition"] = time.gmtime(card.next_rep)
            self._data["avg_thinking_time"] = db.average_thinking_time(card)
            self._data["total_thinking_time"] = db.total_thinking_time(card)
        return self._data


class CurrentCard(StatisticsPage):

    name = _("Current card")

    def __init__(self, component_manager):
        StatisticsPage.__init__(self, component_manager)
        self.html = None
        
    def prepare_statistics(self, variant):
        data = self.get_data()
        self.html = """<html<body>
        <style type="text/css">
        table { height: 100%;
                margin-left: auto; margin-right: auto;
                text-align: center}
        body  { background-color: white;
                margin: 0;
                padding: 0;
                border: thin solid #8F8F8F; }
        </style></head><table><tr><td>"""
        if "error" in data:
            self.html += data["error"]
        else:
            self.html += _("Grade") + ": %d<br>" % data["grade")]
            self.html += _("Easiness") + ": %1.2f<br>" % data["easiness"]
            self.html += _("Repetitions") + ": %d<br>" % data["repetitions"]
            self.html += _("Lapses") + ": %d<br>" % data["lapses"]
            self.html += _("Interval") + ": %d<br>" % data["interval"]
            self.html += _("Last repetition") + ": %s<br>" \
                % time.strftime("%B %d, %Y", data["last_repetition"])           
            self.html += _("Next repetition") + ": %s<br>" \
                % time.strftime("%B %d, %Y", data["next_repetition"])
            self.html += _("Average thinking time (secs)") + ": %d<br>" \
                % data["avg_thinking_time"]
            self.html += _("Total thinking time (secs)") + ": %d<br>" \
                % data["total_thinking_time"]
            self.html += "</td></tr></table></body></html>"

        return self.html

