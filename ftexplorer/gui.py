#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright (c) 2018, CJ Kucera
# All rights reserved.
#   
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the development team nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL CJ KUCERA BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from . import data
from PyQt5 import QtWidgets, QtGui, QtCore

class MainTree(QtWidgets.QTreeView):
    """
    Tree for all our objects
    """

    object_role = QtCore.Qt.UserRole + 1

    def __init__(self, data, display):

        super().__init__()
        self.data = data
        self.display = display

        self.setMinimumWidth(200)
        self.setSelectionBehavior(self.SelectRows)
        self.setHeaderHidden(True)

        self.model = QtGui.QStandardItemModel()
        self.setModel(self.model)

        for item in self.data:
            self.add_to_tree(item, self.model)

    def add_to_tree(self, item, parent):
        """
        Adds the specified item to the specified parent object,
        recursively.
        """
        item_obj = QtGui.QStandardItem(item.name)
        item_obj.setData(item, self.object_role)
        item_obj.setEditable(False)
        for next_item in item:
            self.add_to_tree(next_item, item_obj)
        parent.appendRow([item_obj])

    def selectionChanged(self, selected, deselected):
        """
        What to do when our selection changes.  Mostly just updating
        our label.
        """
        super().selectionChanged(selected, deselected)
        if len(selected.indexes()) > 0:
            node = selected.indexes()[0].data(self.object_role)
            if len(node.data) > 0:
                self.display.setText(''.join(node.data))
            else:
                self.display.setText('(no data)')
        else:
            self.display.setText('(nothing selected)')

class DataDisplay(QtWidgets.QLabel):
    """
    Display area for our data
    """

    def __init__(self):
        super().__init__()
        self.setText('(nothing selected)')
        self.setMargin(10)
        self.setFrameShadow(self.Sunken)
        self.setFrameShape(self.Panel)
        self.setLineWidth(2)
        self.setAutoFillBackground(True)
        self.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)

        # Should figure out how to do this appropriately, rather than
        # just blindly lightening.
        pal = self.palette()
        bgcolor = pal.color(pal.Window)
        pal.setColor(pal.Window, bgcolor.lighter())
        self.setPalette(pal)

    def setText(self, text):
        super().setText('<pre>{}</pre>'.format(text))

class GUI(QtWidgets.QMainWindow):
    """
    Main application window
    """

    def __init__(self, data):
        super().__init__()

        # Store our data
        self.data = data

        # Set some window properties 
        self.setMinimumSize(500, 400)
        self.resize(500, 400)
        self.setWindowTitle('FT Explorer')

        # Set up a QSplitter
        splitter = QtWidgets.QSplitter()

        # Set up our display area and add it to the hbox
        self.display = DataDisplay()
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(self.display)
        scroll.setWidgetResizable(True)

        # Set up our treeview
        self.treeview = MainTree(self.data, self.display)

        # Add both to the splitter
        splitter.addWidget(self.treeview)
        splitter.addWidget(scroll)

        # Set our stretch factors, for when the window is resized
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        # Use the splitter as our main widget
        self.setCentralWidget(splitter)

        # Here we go!
        self.show()

class Application(QtWidgets.QApplication):
    """
    Main application
    """

    def __init__(self):
        """
        Initialization
        """

        super().__init__([])
        self.data = data.Data()
        self.app = GUI(self.data)
