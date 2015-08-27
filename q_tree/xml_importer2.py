import os
import sys
from xml_objectifier import objectifier
from bunch import Bunch

sys.path.append('U:/Data/fiber/fiber_play/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fiber_play.settings')

import django
django.setup()

from q_tree.models import *


#XML_FILE = 'U:/Data/forms_api/forms_api/xmlfiles/Fenland.xml'
XML_FILE = 'U:/Data/pres/fendland-api/fenland_api/xmlfiles/FamHist.xml'
QUESTIONNAIRE_MODEL = False
APP_NAME = 'q_app'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

model_template = """
from django.db import models


class %s(models.Model):
%s # choices
%s # fields
"""

forms_template = """
import floppyforms.__future__ as forms
from .models import %s # import app model


class %sForm(forms.ModelForm): # app model name
    exclude = ['user', 'finished']
    %s # choices
    %s # fields

    class Meta:
        model = %s # app model name
        exclude = ['user', 'finished']
"""

admin_template = """
from django.contrib import admin
from .models import %s
import reversion


class %sAdmin(reversion.VersionAdmin): # app model name
    list_display = ('user', 'finished')

admin.site.register(%s, %sAdmin) # app model name
"""


class ImportApplication(objectifier.Application):

    def import_questionnaire(self):
        data = Bunch()
        data.author = self.author
        data.lang = self.xml_object.attrib['lang']
        data.css = self.xml_object.attrib['css']
        data.version_number = self.version_number
        data.study_name = self.studyname
        data.version_date = self.version_date
        data.title = self.title
        data.subtitle = 'subtitle'
        data.info = 'info'
        data.q_id = 'q_id'
        
        if Questionnaire.objects.filter(q_id=data.q_id).exists():
            print 'No chance' # forces you to cvhange the id on the existing 
            # instance before a new one can be created.
        else:
            q = Questionnaire.objects.create(**data)
            section_keys = []
            self.add_properties(self, q)
            for key in self.sections.keys():
                k = int(key)
                section_keys.append(k)
            section_keys.sort()
            for k in section_keys:
                section = str(k)
                section_data = Bunch()
                section_data.title = 'Section_%s' % k
                section_data.parent = q
                s = Section.objects.create(**section_data)
                self.add_properties(self.sections[section], s)
                # need to order the keys here or change the method
                for qg in self.sections[section].question_groups:
                    qg_data = Bunch()
                    qg_data.position = int(qg.position)
                    qg_data.qg_id = 'qg_id'
                    qg_data.title = 'qg title'
                    qg_data.parent = s
                    new_qg = QuestionGroup.objects.create(**qg_data)
                    self.add_properties(qg, new_qg)
                    for qgo in qg.question_group_objects:
                        if isinstance(qgo, Question):
                            q_data = Bunch()
                            q_data.var_name = qgo.variable
                            q_data.title = qgo.variable
                            q_data.position = int(qgo.position)
                            q_data.parent = new_qg
                            quest = Question.objects.create(**q_data)
                            self.add_properties(qgo, quest)
                        else:
                            tn_data = Bunch()
                            tn_data.t_id = 't_id'
                            try:
                                tn_data.title = qgo.text
                            except:
                                tn_data.title = 'no title'
                            try:
                                tn_data.position = int(qgo.position)
                            except:
                                tn_data.position = -1
                            tn_data.parent = new_qg
                            tn = TextNode.objects.create(**tn_data)
                            self.add_properties(qgo, tn)

    def add_properties(self, obj, model):
        value_dict = {'tdclass': 1, 'qtype': 2, 'endoftr': 3, 'shownumber': 4,
                      'table': 5, 'size': 6, 'search': 7, 'multi': 8}
        try:
            for k in obj.rendering_hints.keys():
                xp = XMLProperty()
                xp.key = value_dict[k]
                xp.value = obj.rendering_hints[k]
                xp.save()
                model.xmlproperty_set.add(xp)
        except:
            pass
        info_dict = {'cssClass': 1}
        print "OBJ: %s" % obj
        try:
            for n in obj.info:
                    ip = InfoProperty()
                    ip.key = 1
                    ip.value = n['cssClass']
                    ip.text = n['text']
                    ip.save()
                    model.infoproperty_set.add(ip)
        except:
            pass
        if isinstance(obj, Question):
            try:
                count = 1
                for opt in obj.template_args['options']:
                    op = OptionProperty()
                    op.position = count
                    count = count + 1
                    op.value = opt['value']
                    op.text = opt['text']
                    op.save()
                    model.optionproperty_set.add(op)
            except:
                pass
    
    def build_app(self, app_name):
        question_objects = []
        section_keys = []
        for key in self.sections.keys():
                k = int(key)
                section_keys.append(k)
        section_keys.sort()
        for k in section_keys:
            for qg in self.sections[str(k)].section_objects:
                question_objects = question_objects + qg.question_group_objects
        fields = ''
        choices = ''
        existing_choices = []
        existing_choices_names = []
        for qo in question_objects:
            if isinstance(qo, Question):
                var_name = qo.variable
                var_type = 'models.CharField'
                data_type = 'string'
                all_args = []
                if 'type' in qo.data_type.keys():
                    var_type = self.get_var_type(qo.data_type['type'])
                    if qo.data_type['type'] == 'string':
                        if 'maxLength' in qo.data_type.keys():
                            if qo.data_type['maxLength'] < 255:
                                var_type = 'models.CharField'
                                all_args.append('max_length=' + qo.data_type['maxLength'])
                            else:
                                var_type = 'models.TextField'
                    data_type = qo.data_type['type']
                else:
                    all_args.append('max_length=200')
                print "FIELD: %s, TYPE: %s" % (var_name, data_type)
                if qo.required == False:
                    all_args.append('blank=True, null=True')
                print "T ARGS: %s" % qo.template_args
                if qo.template_args not in existing_choices and qo.template_args != {'options': []}:
                    existing_choices.append(qo.template_args)
                    existing_choices_names.append(qo.variable)
                    choices = choices + self.get_question_choices(var_name, qo.template_args['options'], data_type)
                    all_args.append('choices=%s_choices' % qo.variable)
                elif qo.template_args != {'options': []}:
                    all_args.append('choices=%s_choices' % existing_choices_names[existing_choices.index(qo.template_args)])
                    
                args_out = ','.join(all_args)
                fields = fields + '\t%s = %s(%s)\n' % (var_name, var_type, args_out)
        with open(APP_NAME+'/models.py', 'w') as f:
            f.write(model_template % (app_name.capitalize(), choices, fields))
        self.build_admin(app_name)
        # self.build_forms(app_name, question_objects, choices)


    def get_question_choices(self, var_name, args_list, var_type):
        result = """\t%s_choices = (%s\t\t)\n\n"""
        choices = '\n'
        if args_list is not None:
            for arg in args_list:
                if var_type in ['integer',]:
                    choices = choices + """\t\t(%s, "%s"),\n""" % (arg['value'], arg['text'])
                else:
                    choices = choices + """\t\t("%s", "%s"),\n""" % (arg['value'], arg['text'])
            return result % (var_name, choices) # sort out tabbing etc.
        return ''
        
    def get_var_type(self, var_type):
        return {'string': 'models.CharField', 'date': 'models.DateField',
                'dateTime': 'models.DateTimeField', 
                'integer': 'models.IntegerField'}[var_type]

    def build_admin(self, app_name):
        with open(APP_NAME+'/admin.py', 'w') as f:
            f.write(admin_template % (app_name.capitalize(), app_name.capitalize(), app_name.capitalize(), app_name.capitalize()))




app = ImportApplication(APP_NAME, XML_FILE)

app.import_questionnaire()


if QUESTIONNAIRE_MODEL:
    d = BASE_DIR + '/' + APP_NAME
    if not os.path.exists(d):
        os.mkdir(APP_NAME)
    app.build_app(APP_NAME)

    
