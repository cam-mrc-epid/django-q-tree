# django-q-tree

##Installation  
Note: This commands below are dependent on Django 1.7 at the moment.  1.8 has changed the argument parsing so that will need fixing.

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
    
##Importing XML
To import xml

        python manage.py importxml <location of xml file> <name>
        
The name is unimportant but must a string.  The file location should be the absolute location of your xml file e.g.
C:/Data/xmlfiles/myfile.xml without any quotes or spaces.  Note the forward slashes.

##App creator  
To create an app from an XML file

        python manage.py buildapp <location of xml file> <appname>
        
This time the name will be the name of the app itself and it will be placed in your project folder.  File location as in the importing xml section above.
