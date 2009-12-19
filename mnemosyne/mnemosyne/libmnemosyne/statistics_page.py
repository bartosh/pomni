#
# statistics_page.py <Peter.Bienstman@UGent.be>
#

from mnemosyne.libmnemosyne.component import Component


class StatisticsPage(Component):

    """A self-contained piece of statistical information, typically displayed
    in the GUI as a page in a tabbed widget.

    Each StatisticsPage can have several 'variants', e.g. displaying the
    number of scheduled cards either for next week or for next month.

    For each StatisticsPage, there will be an associated widget (plotting
    widget, html browser, custom widget, ... ) that is in charge of displaying
    the information. This widget needs to be registered in the component
    manager as a 'statistics_widget' 'used_for' a particular StatisticsPage (or a
    parent class of a StatisticsPage).

    """
    
    component_type = "statistics_page"    
    instantiate = Component.LATER

    name = ""
    variants = [] # [(variant_id, variant_name)]
    show_variants_in_combobox = True

    def __init__(self):
        Component.__init__(self)
        self._data = {}

    def get_data(self):
        """This method returns statistics data."""
        raise NotImplementedError
        
    def prepare_statistics(self, variant_id=None):

        """This method calculates the data for the requested variant and sets
        the approriate hints to be picked up by the corresponding widget.

        """
        raise NotImplementedError


