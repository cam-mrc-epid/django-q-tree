#Project Structure

This a standard Django app which needs to be installed in a project.

The app has the following structure:

**q_tree/management/commands**  This folder contains the management commands for the project.

**q_tree/templates/** contains templates which provide the XML output and also 3 templates that override the admin screens default of django-polymorphic-tree so the checkboxes are available and the copy/paste action will work.

**q_tree/admin.py** contains the admin screen set up.  It also contains the copy/paste admin action function.

**q_tree/models.py** contains the models for the project.  They subclass django-polymorphic-tree models.  A BaseTreeNode class is the superclass for the Questionnaire, Section, QuestionGroup and Question classes.  This common class is used in the admin.  Admin change-lists work for a single model and in the this case we use the BaseTreeNode model so that we can list all our object types in a single view.  The BaseTreeNode has 2 custom model managers.  One provided by django-polymorphic-tree and another from model_utils which allows the copy/paste function to access subclasses from the BaseTreeNode superclass for admin actions.

**q_tree/views.py** contains a single view that outputs the XML for the given Q id of a questionnaire (see Usage).

