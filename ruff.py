from PySide2 import QtWidgets, QtCore, QtGui
import typing

class MyButton(QtWidgets.QPushButton):
    @typing.overload
    def __init__(self, value: type, icon: typing.Union[QtGui.QIcon, QtGui.QPixmap], text: str, parent: typing.Optional[QtWidgets.QWidget] = ...,) -> None:
        ...

    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.foo = value


app = QtWidgets.QApplication()
b= MyButton("val", "testo")
print(b.foo)
b.show()

app.exec_()
