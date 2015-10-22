# django-q-tree

##Installation  
Note: This commands below are dependent on Django 1.7 at the moment.  1.8 has changed the argument parsing so that will need fixing.

Install the objectifier dependency.

    pip install git+git://github.com/cam-mrc-epid/xml-objectifier
    
    pip install git+git://github.com/cam-mrc-epid/django-q-tree
    
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

##Exporting XML
To export xml

        python manage.py exportxml <q_id> 

where `<q_id>` is the Questionnaire's Q id.  You will see this value in the Questionnaire's admin interface.  You can set it to what you want.  This will output XML to standard output. It can be saved to a file like this

        python manage.py exportxml <q_id> > SomeFile.xml  

The XML can be renderered via a browser and saved in that way using the url

        http://some-server:port/xml_out.xml?id=<q_id>
        
This requires the url to be set up in your project urls.py

```python
url(r'^xml_out.xml/', 'q_tree.views.xml_view'),
```

where the q_id is the Questionnaire Q id value which can be set in the admin interface.      

##App creator  
The idea of the app creator was the possibility of generating a Django app direct from XML.  This is not really possible as TextNodes often provide labels that are not attached to the Question.  This function will build models for the XML file's questions and also integrate it into the admin interface.  It would be possible to build django forms direct from the XML if labels attached to the questions.

To create an app from an XML file

        python manage.py buildapp <location of xml file> <appname>
        
This time the name will be the name of the app itself and it will be placed in your project folder.  File location as in the importing xml section above.
