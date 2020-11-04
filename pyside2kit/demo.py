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
                                         palette_size=800,
                                         image_filename=os.path.join(os.path.dirname(__file__), "resources", "palette_01.png"),
                                         button_labels_filename=os.path.join(os.path.dirname(__file__), "resources", "labels_01.txt"))
    demo_layout.addWidget(my_palette)

    change_labels_btn = QtWidgets.QPushButton("Change palette labels")
    demo_layout.addWidget(change_labels_btn)
    change_labels_btn.setEnabled(False)

    my_list = ps2kit.QCheckableList("Items", ("item1", "item2", "item3", "item4", "item5", "item6"))
    demo_layout.addWidget(my_list)
    change_items_list_button = QtWidgets.QPushButton("Update Items (generate a random list of strings)")
    change_items_list_button.clicked.connect(lambda: my_list.update_items(tuple([random_string(random.randrange(4, 16)) for i in range(random.randrange(1, 10))])))
    demo_layout.addWidget(change_items_list_button)

    my_browse = ps2kit.QBrowseFolder(root_folder="C:\\")
    my_browse.title = "My folder browser dialog"
    demo_layout.addWidget(my_browse)

    my_file_browse = ps2kit.QBrowseFile(root_folder="C:\\")
    my_file_browse.title = "My file browser dialog"
    demo_layout.addWidget(my_file_browse)

    demo_window.setLayout(demo_layout)

    demo_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":  # Local Run
    import ps2kit
    run_demo()
else:  # Module Run, When going production - delete if/else
    from . import ps2kit
