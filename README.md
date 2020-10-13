# pyside2-kit
**A kit of pre-made objects for your PySide 2 user interfaces**

## Introduction
While writing my small tools I found myself building some parts of the UIs that could be used in other projects.
So instead of _reinventig the wheel_ I thought to create a ps2kit.py module containing all of them.

It's an ongoing process: I plan to add objects to the module as soon as they pops out in another project.

All objects are classes that extend some other standard PySide2 class (I think they'll be some kind of QWidget in 99% of the cases)

## Demo script
Run demo.py to open a showcase window.
**NOTE** At the moment the *Change palette image* works only the first time (still have to cycle between template images) and *Change palette labels* is deactivated because the function is not implemented yet.

## Module content
### QTexturePalette

This widget shows a squared image and overlays on top of it a grid of squadred, transparent `QPushButtons`, each one with an optional label.
I used this widget to select cells from a texture palette and assign texture/color data to a 3D object in Blender.
Every `QPushButton` of the grid is connected to the same **@Slot** function `press_button()`:
the function emit a signal containing the informatin needed to identify the source button and take appropriate actions in the main UI/application.

### QCheckableList

This widget shows a list text item with checkboxes and 2 button for select All/None.
The list of texts to be shown is provided with a Tuple.
It uses a QTreeWidget to show the checkable item.

### QBrowseFolder

This widget is composed by a line edit and a 'browse' button: used for selecting a folder and get its path
