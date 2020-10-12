import sys
import os

import random
import string

from PySide2 import QtWidgets


def random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def run_demo():
    app = QtWidgets.QApplication([])
    demo_window = QtWidgets.QWidget()
    demo_layout = QtWidgets.QVBoxLayout()
    my_palette = ps2kit.QTexturePalette(palette_name="Test Palette", grid_side=8,
                                         image_filename=os.path.join(os.path.dirname(__file__), "resources", "palette_01.png"),
                                         palette_size=800,
                                         button_labels_filename=os.path.join(os.path.dirname(__file__), "resources", "labels_01.txt"))
    demo_layout.addWidget(my_palette)
    change_palette_btn = QtWidgets.QPushButton("Change palette image")
    demo_layout.addWidget(change_palette_btn)

    change_palette_btn.clicked.connect(lambda: my_palette.change_image(os.path.join(os.path.dirname(__file__), "resources", "palette_02.png")))
    change_labels_btn = QtWidgets.QPushButton("Change palette labels")
    demo_layout.addWidget(change_labels_btn)

    my_list = ps2kit.QCheckableList("Items", ("item1", "item2", "item3", "item4", "item5", "item6"))
    demo_layout.addWidget(my_list)

    test_button = QtWidgets.QPushButton("Update Items (generate a random list of strings)")
    test_button.clicked.connect(lambda: my_list.update_items(tuple([random_string(random.randrange(4, 16)) for i in range(random.randrange(1, 10))])))

    demo_layout.addWidget(test_button)
    demo_window.setLayout(demo_layout)

    demo_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":  # Local Run
    import ps2kit
    run_demo()
else:  # Module Run, When going production - delete if/else
    from . import ps2kit
