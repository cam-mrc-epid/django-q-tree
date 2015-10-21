#XML Editor

This is a prototype editor for the XML files.  It converts XML into a tree structure.  The tree structure has various class types that provides different properties for the various parts of the tree, Sections, Question Groups, Questions, etc.  These objects have a BaseTreeNode superclass which is used in the admin views.  Admin change-lists normally work with a single model type and in this case it is the BaseTreeNode model we use to set up the admin interface.  All our objects are of this type.  

The admin views allow copy and paste of tree objects and also drag and drop.  

There are 3 management functions described in the Usage section which can import and export xml.  It is also possible to render a questionnaire's XML in the browser.  An additional feature is the `buildapp` command which will create a basic Django app and build models to match the question in the XML and a basic admin set up as well.  It was not possible to build Django forms automatically at this stage because TextNode labels have no connection to Questions.  If TextNode were connected to Questions it would be possible to build Django Forms automatically.  These forms can render their own HTML automatically which could be useful in some cases.  They can also provide validation.

##Issues

In building this structure, some identifier had to be used so that the tree objects have an indentifier of some kind in the admin interface.  I have used a title for this but many things in the XML don't have titles.  I have in some cases put in a title so that the objects can be used in the Admin interface.  The problem being that exported XML has this false title in it.  This would require some decisions to fix about what the identifier should be and how it would be stripped out of the output if it shouldn't be there.  The importxml functions and classes are in the management/commands folder and subclass the XML Objectifier's class.  This subclass provides a few functions to convert the XML Objectifiers objects into the new tree structure objects described in this project's models.py.
