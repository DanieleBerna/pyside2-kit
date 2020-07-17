#from . import qtutils
import sys
import os
from PySide2 import QtWidgets


def run_demo():
    app = QtWidgets.QApplication([])
    demo_window = QtWidgets.QWidget()
    demo_layout = QtWidgets.QVBoxLayout()
    my_palette = ps2kit.QTexturePalette(palette_name="Test Palette", grid_side=8,
                                         image_path=os.path.join(os.path.dirname(__file__), "resources", "palette_01.png"),
                                         palette_size=800,
                                         button_labels_filename=os.path.join(os.path.dirname(__file__), "resources", "labels_01.txt"))
    demo_layout.addWidget(my_palette)
    change_palette_btn = QtWidgets.QPushButton("Change palette image")
    demo_layout.addWidget(change_palette_btn)
    change_labels_btn = QtWidgets.QPushButton("Change palette labels")
    demo_layout.addWidget(change_labels_btn)
    demo_window.setLayout(demo_layout)

    demo_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__": # Local Run
    import ps2kit
    run_demo()
else: # Module Run, When going production - delete if/else
    from . import ps2kit


