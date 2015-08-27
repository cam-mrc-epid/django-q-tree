=============
Q Tree Editor
=============

This is an app to edit Forms System XML.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "q_tree" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'polls',
    )

2. Run `python manage.py migrate` to create the q_tree models.

3. Start the development server and visit http://127.0.0.1:8000/admin/
   to create or import an XML file.

4. Visit /admin to edit q_tree XML.
