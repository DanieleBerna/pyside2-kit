"""Based on code by Dhruv Govil"""

from PySide2 import QtWidgets, QtCore
import sys


class QCheckableList(QtWidgets.QWidget):
    """
        Extends QWidget to create a clickable palette.
        A QCheckableList object is composed by a group and a QTreeWidget used as list of items, each with a checkbox.
        """
    def __init__(self, title, items=()):
        super(QCheckableList, self).__init__()

        self.items = items

        layout = QtWidgets.QGridLayout(self)

        group = QtWidgets.QGroupBox(title)
        group_layout = QtWidgets.QVBoxLayout(group)
        layout.addWidget(group, 0, 0, 3, 3)

        tree = self.tree = QtWidgets.QTreeWidget()
        tree.setHeaderHidden(True)
        group_layout.addWidget(tree)

        for i in self.items:
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, i)
            item.setCheckState(0, QtCore.Qt.Unchecked)
            tree.addTopLevelItem(item)

        test_button = QtWidgets.QPushButton("Button")
        test_button.clicked.connect(self.update_items)
        layout.addWidget(test_button, 3, 1)

    def get_selected_items(self):
        root = self.tree.invisibleRootItem()
        selected_items = []
        selected_items_texts = []
        for i in range(root.childCount()):
            item = root.child(i)
            if item.checkState(0):
                selected_items.append(item)
                selected_items_texts.append(item.text(0))

        return selected_items, selected_items_texts

    def update_items(self):
        root = self.tree.invisibleRootItem()
        for item in root.takeChildren():
            root.removeChild(item)

        for i in self.items:
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, i)
            item.setCheckState(0, QtCore.Qt.Unchecked)
            self.tree.addTopLevelItem(item)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    items = ("monitor", "mouse", "keyboard", "pippo", "pluto", "paperino", "topolino", "belin", "belan")
    w = QCheckableList("prova", items)
    w.show()

    sys.exit(app.exec_())

