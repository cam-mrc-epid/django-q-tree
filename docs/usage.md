#Usage

##Admin Interface
You can create Questionnaire, Section, etc. objects via the Admin interface.  These can be copy'n pasted and drag and dropped around the interface.  At present the copy/paste pastes a single object in place and does not include the children.  I don't think it would be a big job to add this functionality.  I'll give it a go if I have time.

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

        http://some-server:port/xml_out.xml?q_id=<q_id>

where the q_id is the Questionnaire Q id value which can be set in the admin interface.      

##App creator  
The idea of the app creator was the possibility of generating a Django app direct from XML.  This is not really possible as TextNodes often provide labels that are not attached to the Question.  This function will build models for the XML file's questions and also integrate it into the admin interface.  It would be possible to build django forms direct from the XML if labels attached to the questions.

To create an app from an XML file

        python manage.py buildapp <location of xml file> <appname>
        
This time the name will be the name of the app itself and it will be placed in your project folder.  File location as in the importing xml section above.
