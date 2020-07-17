__version__ = '0.1'
__author__ = 'Daniele Bernardini'

from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Signal, Slot
from functools import partial


class QTexturePalette(QtWidgets.QGroupBox):
    """
    Extends QGroupBox to create a clickable palette.
    A QTexturePalette object is composed by a group and a grid of transparent QPushButton overlayed to an image.
    """
    button_pressed = Signal(str, float, bool, bool, bool)  # Signal emitted when any button is pressed

    @Slot(float, int)
    def press_button(self, button_value, button_index):
        """
        Slot function connected to the clicked signal of the QPushButtons in the grid.
        It emits another signal to the application containing all the informations about the interaction happened.
        :param button_value: the specific value associate do the pressed button
        """
        self.last_pressed_button_index = button_index
        self.button_pressed.emit(self.palette_name, button_value,
                                 (QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.AltModifier),
                                 (QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier),
                                 (QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier))

    def __init__(self, palette_name="", grid_side=4, image_path="", palette_size=800, button_labels_filename=None):
        """
        Setup the palette object generating the QPushButton grid
        :param palette_name: name of the palette and of the group
        :param grid_side: number of cells/button per side (assuming a grid_side x grid_side palette)
        :param image_path: filepath of the image to be used
        :param palette_size: size in pixel of the widget
        """
        image_path = image_path.replace("\\", "/")
        if button_labels_filename is not None:
            button_labels_filename = button_labels_filename.replace("\\", "/")
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

        temp_app = QtWidgets.QApplication.instance()
        if temp_app is None:
            # if it does not exist then a QApplication is created
            temp_app = QtWidgets.QApplication([])
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

                temp_btn.setToolTip("Click: paint\nAlt+click: select\nAlt+Shift+click: add to selection\nAlt+Ctrl+click: intersect selections")
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
        self.palette_frame.setStyleSheet(".QFrame{border-image: url( " + image_path + ") 0 0 0 0 stretch stretch;}")
        self.palette_group_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.palette_group_layout.addWidget(self.palette_frame)
        self.setLayout(self.palette_group_layout)
        # self.setBaseSize(palette_size, palette_size)
        self.setSizePolicy(QtWidgets.QSizePolicy().Expanding, QtWidgets.QSizePolicy().Expanding)

    def change_image(self, image_path):
        self.palette_frame.setStyleSheet(".QFrame{border-image: url( " + image_path + ") 0 0 0 0 stretch stretch;}")

    def change_labels(self, button_labels_filename):
        pass

