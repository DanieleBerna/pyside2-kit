# pyside2-kit
**A kit of pre-made objects for your PySide 2 user interfaces**

## Introduction
While writing my small tools I found myself building some parts of the UIs that could be used in other projects.
So instead of _reinventig the wheel_ I thought to create a ps2kit.py module containing all of them.

It's an ongoing process: I plan to add objects to the module as soon as they pops out in another project.

All objects are classes that extend some other standard PySide2 class (I think they'll be some kind of QWidget in 99% of the cases)

## Demo script
Run demo.py to open a showcase window.

## Module content
### QTexturePalette

This widget shows a squared image and overlays on top of it a grid of squadred, transparent `QPushButtons`, each one with an optional label.
I used this widget to select cells from a texture palette and assign texture/color data to a 3D object in Blender.
Every `QPushButton` of the grid is connected to the same **@Slot** function `press_button()`:
the function emit a signal containing the informatin needed to identify the source button and take appropriate actions in the main UI/application.
It's possible to change the image file using the QBrowseFile widget included.

### QCheckableList

This widget shows a list text item with checkboxes and 2 button for select All/None.
The list of texts to be shown is provided with a Tuple.
It uses a QTreeWidget to show the checkable item.

### QBrowseFolder

A widget that opens a QFileDialog.getExistingDirectory: used to get the path of an existing folder.
It's composed by a line edit (optional) that shows the folder path and a 'browse' button used to open the dialog.


### QBrowseFile

A widget that opens a QFileDialog.getOpenFileName: used to get the path of a file to be opened.
It's composed by a line edit (optional) that shows the file path and a 'select' button used to open the dialog.


### QSaveFile

A widget that opens a QFileDialog.getSaveFileName: used to get the path of a file to be saved.
It's composed by a line edit (optional) that shows the file path and a 'save' button used to open the dialog.
