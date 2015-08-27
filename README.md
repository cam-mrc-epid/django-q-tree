# django-q-tree

##Installation  
Install the objectifier dependency.

    pip install git+git://github.com/davidgillies/xml-objectifier
    
    pip install git+git://github.com/davidgillies/django-q-tree
    
Add the following to your INSTALLED_APPS in your django project settings

    'q_tree',
    'polymorphic',
    'polymorphic_tree',
    'mptt',
    
Run migrations
    
    python manage.py migrate
    
