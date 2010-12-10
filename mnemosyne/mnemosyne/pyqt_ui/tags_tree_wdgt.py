#
# tags_tree_wdgt.py <Peter.Bienstman@UGent.be>
#

from PyQt4 import QtCore, QtGui

from mnemosyne.libmnemosyne.translator import _
from mnemosyne.libmnemosyne.tag import TagsTree
from mnemosyne.libmnemosyne.component import Component


class TagsTreeWdgt(QtGui.QWidget, Component):

    """Displays all the tags in a tree together with check boxes."""

    def __init__(self, component_manager, parent):
        Component.__init__(self, component_manager)
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QVBoxLayout(self)
        self.tags_tree = QtGui.QTreeWidget(self)
        self.tags_tree.setHeaderHidden(True)
        self.layout.addWidget(self.tags_tree)


    def create_subtree(self, qt_parent, subtree):
        for node in subtree:
            if type(node) == type([]):
                # Create Qt node item.
                node_item = 0
                self.create_subtree(qt_parent=node_item, node)
            else:
                # Create Qt leaf item
                leaf_item = 0
        
    def display(self, criterion):
        self.tags_tree.clear()

        _tags_tree = TagsTree(self.component_manager)
        parent = _tag_tree.tree["__ALL__"]
        # create parent node
        for nodes in parent
        

        
        
        self.tag_for_node_item = {}
        root_item = QtGui.QTreeWidgetItem(self.tags_tree, [_("All tags")], 0)
        root_item.setFlags(root_item.flags() | \
           QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsTristate)
        root_item.setCheckState(0, QtCore.Qt.Checked)
        self.tag_for_node_item = {}
        node_item_for_partial_tag = {} # Not needed if libmnemosyne takes over?
        for tag in self.database().tags():
            if tag.name == "__UNTAGGED__":
                tag.name = _("Untagged")
            parent = root_item
            partial_tag = ""
            node_item = None
            for node in tag.name.split("::"):
                node += "::"
                partial_tag += node
                if partial_tag not in node_item_for_partial_tag:
                    node_item = QtGui.QTreeWidgetItem(parent, [node[:-2]], 0)
                    node_item.setFlags(node_item.flags() | \
                        QtCore.Qt.ItemIsUserCheckable | \
                        QtCore.Qt.ItemIsTristate)
                    node_item_for_partial_tag[partial_tag] = node_item
                parent = node_item_for_partial_tag[partial_tag]
            self.tag_for_node_item[node_item] = tag
        # Set forbidden tags.
        if len(criterion.forbidden_tag__ids):
            for node_item, tag in self.tag_for_node_item.iteritems():
                if tag._id in criterion.forbidden_tag__ids:
                    node_item.setCheckState(0, QtCore.Qt.Checked)
                else:
                    node_item.setCheckState(0, QtCore.Qt.Unchecked)  
        # Set active tags.
        else:
            for node_item, tag in self.tag_for_node_item.iteritems():
                if tag._id in criterion.active_tag__ids:
                    node_item.setCheckState(0, QtCore.Qt.Checked)
                else:
                    node_item.setCheckState(0, QtCore.Qt.Unchecked)
        # Finalise.
        self.tags_tree.expandAll()

    def selection_to_active_tags_in_criterion(self, criterion):
        for item, tag in self.tag_for_node_item.iteritems():
            if item.checkState(0) == QtCore.Qt.Checked:
                criterion.active_tag__ids.add(tag._id)
        criterion.forbidden_tags = set()
        return criterion

    def selection_to_forbidden_tags_in_criterion(self, criterion):
        for item, tag in self.tag_for_node_item.iteritems():
            if item.checkState(0) == QtCore.Qt.Checked:
                criterion.forbidden_tag__ids.add(tag._id)
        criterion.active_tags = set(self.tag_for_node_item.values())
        return criterion
    
