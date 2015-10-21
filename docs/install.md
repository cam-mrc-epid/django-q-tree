#Installation

Note: This commands below are dependent on Django 1.7 at the moment.  1.8 has changed the argument parsing so that will need fixing.

Install the objectifier dependency.

    pip install git+git://github.com/davidgillies/xml-objectifier

Install the Editor app.
    
    pip install git+git://github.com/davidgillies/django-q-tree
    
Add the following to your INSTALLED_APPS in your django project settings

    'q_tree',
    'polymorphic',
    'polymorphic_tree',
    'mptt',
    
Run migrations
    
    python manage.py migrate

To be able to view the XML via the browser you need to add the following url to your project urls.py

```python
url(r'^xml_out.xml/', 'q_tree.views.xml_view'),
```
