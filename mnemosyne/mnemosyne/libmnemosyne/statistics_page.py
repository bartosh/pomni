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
        
    def prepare_statistics(self, variant_id):

        """This method calculates the data for the requested variant and sets
        the approriate hints to be picked up by the corresponding widget.

        """
        
        raise NotImplementedError


class PlotStatisticsPage(StatisticsPage):

    """A statistics page where the data is represented on a graphical plot.

    Most variables here have a relatively plotting toolkit independent meaning,
    except for 'extra_hints', which currently is being used as the **kwargs
    variable from matplotlib.

    """
        
    def __init__(self, component_manager):
        StatisticsPage.__init__(self, component_manager)
        self.data = None
        self.plot_type = "" # barchart, histogram, piechart, linechart
        self.title = ""
        self.xlabel = ""
        self.ylabel = ""
        self.xvalues = []
        self.xticks = []
        self.xticklabels = []
        self.show_text_value = True # Show value above each bar in barchart.
        self.extra_hints = {}


class HtmlStatisticsPage(StatisticsPage):

    "A statistics page which generates html to displayed in a browser widget."
        
    def __init__(self, component_manager):
        StatisticsPage.__init__(self, component_manager)
        self.html = None

