# -*- coding: utf-8 -*-

"""
ps2kit is a module containing pre-built PySide2 objects useful for creating more complex UI
Each object is built on standard PySide2 classes like QWidget.

"""

from functools import partial

from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Signal, Slot


class QTexturePalette(QtWidgets.QGroupBox):
    """
    Extends QGroupBox to create a clickable palette.
    A QTexturePalette object is composed by a group and a grid of transparent QPushButton overlaid to an image.
    """
    button_pressed = Signal(str, float, bool, bool, bool)  # Signal emitted when a button is pressed
    """
    Signal arguments:
    (str) palette name, (float) value associated to the button, (bool) is Alt pressed, (bool)is Shift pressed, (bool)is Ctrl pressed
    """

    @Slot(float, int)
    def press_button(self, button_value, button_index):
        """
        Slot function connected to the clicked signal of the QPushButtons in the grid.
        It emits another signal to the main application/UI together with all the information about the interaction happened.
        :param button_value: the specific value associate do the pressed button
        :param button_index: list index of the pressed button
        """
        self.last_pressed_button_index = button_index  # Needed to highlight the last button
        self.button_pressed.emit(self.palette_name, button_value,
                                 (QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.AltModifier),
                                 (QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier),
                                 (QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier))

    def __init__(self, palette_name="", grid_side=4, image_filename="", button_labels_filename=None, palette_size=800, buttons_tooltip="Tooltip"):
        """
        Setup the palette object generating the QPushButton grid
        :param palette_name: name of the palette: it will shown as group name too
        :param grid_side: number of cells/button per side (assuming a squared grid_side x grid_side palette)
        :param image_filename: full filename with path of the image to be used as palette background
        :param button_labels_filename: full filename with path of the optional text file containing buttons' labels
        :param palette_size: size in pixel of the widget
        :param buttons_tooltip: tooltip text for the buttons (note: same for all)
        """
        image_filename = image_filename.replace("\\", "/")  # Needed because path ends in a stylesheet
        if button_labels_filename is not None:
            button_labels_filename = button_labels_filename.replace("\\", "/")  # Needed because path ends in a stylesheet

        super(QTexturePalette, self).__init__(palette_name)

        self.palette_name = palette_name
        self.palette_group_layout = QtWidgets.QHBoxLayout()
        self.palette_frame = QtWidgets.QFrame()
        self.palette_frame_layout = QtWidgets.QGridLayout()
        self.palette_frame_layout.setSpacing(0)
        self.palette_frame_layout.setMargin(0)
        self.palette_frame.setFrameStyle(QtWidgets.QFrame.Box)
        self.palette_frame.setLineWidth(0)
        self.palette_frame.setLayout(self.palette_frame_layout)
        self.grid_side = grid_side  # How many buttons per row
        self.grid_step = 1.0 / (self.grid_side * self.grid_side)  # step increment of button values
        self.palette_buttons = []  # list of all QPushButtons
        self.last_pressed_button_index = None
        self.palette_buttons_group = QtWidgets.QButtonGroup()
        self.palette_buttons_group.setExclusive(True)

        # Here a size multiplier is computed for screen resolutions < 4k. Used for scale fonts and widgets
        temp_app = QtWidgets.QApplication.instance()
        if temp_app is None:
            temp_app = QtWidgets.QApplication([])  # if it does not exist then a QApplication is created
        self.screen_factor = (2160/temp_app.primaryScreen().size().height())

        # Initialize button labels list reading labels from a given txt file
        self.button_labels_list = []
        if button_labels_filename is not None:
            try:
                self.button_labels_list = [line.rstrip('\n') for line in open(button_labels_filename)]
            except IOError:
                pass

        for i in range(self.grid_side):
            for j in range(self.grid_side):
                button_value = (self.grid_step * ((j + 1) + (self.grid_side * i) - 1))
                button_label = ""
                try:
                    button_label = self.button_labels_list[((j + 1) + (self.grid_side * i) - 1)]
                except LookupError:
                    pass

                temp_label = QtWidgets.QLabel(button_label)
                temp_label.setAlignment(QtCore.Qt.AlignCenter)

                temp_label.setStyleSheet(".QLabel {color: white;font-size: "+str(round(15/self.screen_factor))+"px; border:0px; border-width: 0px}")
                temp_layout = QtWidgets.QVBoxLayout()
                temp_layout.setContentsMargins(1, 1, 1, 1)
                temp_layout.addWidget(temp_label)
                temp_label.setWordWrap(True)
                temp_btn = QtWidgets.QPushButton("")

                temp_btn.setToolTip(buttons_tooltip)
                temp_btn.setMinimumSize(round(palette_size // grid_side / self.screen_factor), round(palette_size // grid_side / self.screen_factor))
                temp_btn.setFlat(True)
                temp_btn.setCheckable(True)
                temp_btn.autoRaise = False
                temp_btn.setStyleSheet(".QPushButton{background-color: transparent;padding: 0px}"
                                       ".QPushButton:hover{background-color: transparent;border-style: inset;border-width: 2px;border-color: blue;}"
                                       ".QPushButton:pressed{background-color: transparent;border-style: inset;border-width: 3px;border-color: grey;}"
                                       ".QPushButton:checked{background-color: transparent;border-style: inset;border-width: 1px;border-color: white;}")
                temp_btn.setSizePolicy(QtWidgets.QSizePolicy().Expanding, QtWidgets.QSizePolicy().Expanding)
                self.palette_buttons.append((temp_btn, button_value))
                temp_btn.setLayout(temp_layout)
                self.palette_frame_layout.addWidget(temp_btn, i, j, 1, 1)
                temp_btn.clicked.connect(partial(self.press_button, button_value, len(self.palette_buttons)-1))
                self.palette_buttons_group.addButton(temp_btn)

        self.palette_frame.setAutoFillBackground(True)
        self.palette_frame.setSizePolicy(QtWidgets.QSizePolicy().Expanding, QtWidgets.QSizePolicy().Expanding)
        self.palette_frame.setStyleSheet(".QFrame{border-image: url( " + image_filename + ") 0 0 0 0 stretch stretch;}")
        self.palette_group_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.palette_group_layout.addWidget(self.palette_frame)
        self.setLayout(self.palette_group_layout)
        self.setSizePolicy(QtWidgets.QSizePolicy().Expanding, QtWidgets.QSizePolicy().Expanding)

    def change_image(self, image_filename):
        """
        Update the background image of the palette
        :param image_filename: full path and name of the new image
        """
        image_filename = image_filename.replace("\\", "/")  # Needed because path ends in a stylesheet
        self.palette_frame.setStyleSheet(".QFrame{border-image: url( " + image_filename + ") 0 0 0 0 stretch stretch;}")

    def change_labels(self, button_labels_filename):
        """
        Update the buttons' labels
        :param button_labels_filename:
        """
        # TODO
        pass


class QCheckableList(QtWidgets.QWidget):
    """
        Extends QWidget to create a clickable palette.
        A QCheckableList object is composed by a group and a QTreeWidget used as list of items, each with a checkbox.
        """
    def __init__(self, title, items=(), show_buttons=True):
        """
        Class constructor
        :param title: Name of the palette widget
        :param items: tuple containing the texts to be listed
        :param show_buttons: (bool) Show All/None selection buttons
        """
        super(QCheckableList, self).__init__()

        self.items = items

        layout = QtWidgets.QGridLayout(self)

        group = QtWidgets.QGroupBox(title)
        group_layout = QtWidgets.QVBoxLayout(group)
        layout.addWidget(group, 0, 0, 3, 3)

        if show_buttons:
            selection_buttons_layout = QtWidgets.QHBoxLayout()
            self.select_all_btn = QtWidgets.QPushButton("All")
            self.select_all_btn.clicked.connect(partial(self.set_items_status, True))
            selection_buttons_layout.addWidget(self.select_all_btn)
            self.select_none_btn = QtWidgets.QPushButton("None")
            self.select_none_btn.clicked.connect(partial(self.set_items_status, False))
            selection_buttons_layout.addWidget(self.select_none_btn)
            group_layout.addLayout(selection_buttons_layout)

        tree = self.tree = QtWidgets.QTreeWidget()
        tree.setHeaderHidden(True)
        group_layout.addWidget(tree)

        for i in self.items:
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, i)
            item.setCheckState(0, QtCore.Qt.Unchecked)
            tree.addTopLevelItem(item)

    def set_items_status(self, checked):
        """
        Set checked status for the items
        :param checked: (bool) Is the item checked or not?
        """
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            if checked:
                item.setCheckState(0, QtCore.Qt.Checked)
            else:
                item.setCheckState(0, QtCore.Qt.Unchecked)

    def get_selected_items(self):
        """
        Get checked items
        :return: (tuple) lists of selected items and selected items texts
        """
        root = self.tree.invisibleRootItem()
        selected_items = []
        selected_items_texts = []
        for i in range(root.childCount()):
            item = root.child(i)
            if item.checkState(0):
                selected_items.append(item)
                selected_items_texts.append(item.text(0))

        return selected_items, selected_items_texts

    @Slot(tuple)
    def update_items(self, new_items):
        """
        Change the list of shown items
        :param new_items: (tuple) a new tuple os items to be shown
        """
        root = self.tree.invisibleRootItem()
        for item in root.takeChildren():
            root.removeChild(item)

        self.items = new_items[:]
        for i in self.items:
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, i)
            item.setCheckState(0, QtCore.Qt.Unchecked)
            self.tree.addTopLevelItem(item)
