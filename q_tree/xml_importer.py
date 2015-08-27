import os
import sys


sys.path.append('U:/Data/fiber/fiber_play/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fiber_play.settings')

import django
django.setup()

from lxml import objectify
from bunch import Bunch
import datetime
from q_tree.models import *


#XML_FILE = 'U:/Data/forms_api/forms_api/xmlfiles/Fenland.xml'
XML_FILE = 'U:/Data/pres/fendland-api/fenland_api/xmlfiles/FamHist.xml'
xml_string = open(XML_FILE, 'r').read()
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


class MethodMixin(object):
    def set_rendering_hint(self, item):
        key = item.rhType.text
        self.rendering_hints[key] = ''
        for rhdata in item.rhData:
            self.rendering_hints[key] = self.rendering_hints[key] + ' ' + str(rhdata)
        self.rendering_hints[key] = self.rendering_hints[key].strip()

    def tag_type(self, tag_type):
        return {'{http://www.mrc-epid.cam.ac.uk/schema/common/epi}title': self.set_title, 
                '{http://www.mrc-epid.cam.ac.uk/schema/common/epi}info': self.set_info,
                '{http://www.mrc-epid.cam.ac.uk/schema/common/epi}renderingHint': self.set_rendering_hint,
                '{http://www.mrc-epid.cam.ac.uk/schema/common/epi}externalPrograms': self.set_external_programs,
                '{http://www.mrc-epid.cam.ac.uk/schema/common/epi}option': self.set_options,
                '{http://www.mrc-epid.cam.ac.uk/schema/common/epi}restrictions': self.set_restrictions,
                '{http://www.mrc-epid.cam.ac.uk/schema/common/epi}textNode': self.set_text_node,
                '{http://www.mrc-epid.cam.ac.uk/schema/common/epi}question': self.set_question,
                '{http://www.mrc-epid.cam.ac.uk/schema/common/epi}questionGroup':self.set_question_group,
                '{http://www.mrc-epid.cam.ac.uk/schema/common/epi}variable': self.set_variable
                }[tag_type]

    def __str__(self):
        return "%s: %s" % (self.title, self.position)

    def __unicode__(self):
        return "%s: %s" % (self.title, self.position)

    def set_title(self, item):
        pass

    def set_variable(self, item):
        pass

    def set_options(self, item):
        pass

    def set_info(self, item):
        pass

    def set_external_programs(self, item):
        pass

    def set_text_node(self, item):
        pass

    def set_question(self, item):
        pass

    def set_question_group(self, item):
        pass

    def set_restrictions(self, item):
        pass


class ImportQuestion(MethodMixin):
    def __init__(self, question_object, app_object, section_object):
        self.app_object = app_object
        self.question_objects = []
        self.section = section_object
        self.title = question_object.attrib['position']
        self.variable = question_object.variable.varName.text
        self.var_value = None
        self.var_id = None
        self.required = False
        self.info = []
        self.dynamic = False
        self.maxlength = 0
        self.multi = False
        self.tests = []
        self.data_type = {}
        self.pattern = ''
        self.id = question_object.attrib['ID']
        self.position = question_object.attrib['position']
        self.rendering_hints = {}
        self.restrictions = {}
        self.template = ''
        self.template_args = {'options': []}
        self.model = None
        self.build_question(question_object)
        self.validator_rules()

    def validator_rules(self):
        rules = {}
        try:
            rules['type'] = self.data_type['type']
            self.tests.append('type')
            try:
                self.pattern = self.data_type['pattern']
            except:
                pass
        except:
            pass
        if 'CheckMaxLength' in self.restrictions.keys():
            rules['CheckMaxLength'] = self.data_type['maxLength']
            self.maxlength = self.data_type['maxLength']
            self.tests.append('CheckMaxLength')
        if 'IsAnswered' in self.restrictions.keys():
            if self.restrictions['IsAnswered']['AllowError'] == 'false':
                rules['IsAnswered'] = True
                self.required = True
                self.tests.append('IsAnswered')
        return rules

    def get_template(self, selection):
        return {'radio': 'html_renderer/radio.html',
                'dropdown': 'html_renderer/select.html',
                'text': 'html_renderer/text.html',
                'multiline': 'html_renderer/textarea.html',
                'range': 'html_renderer/range.html',
                'datalist': 'html_renderer/datalist.html',
                'search': 'html_renderer/search.html'}[selection]

    def set_template(self):
        self.template = self.get_template(self.rendering_hints['qtype'])

    def build_question(self, question_object):
        for item in question_object.getchildren():
            self.tag_type(item.tag)(item)
        self.set_template()

    def set_options(self, item):
        try:
            if item.optionText.text == 'dynamic':
                self.template_args['options'] = self.get_options(item.optionValue.text)
                self.dynamic = True
            else:
                self.template_args['options'].append({'text': item.optionText.text, 'value': item.optionValue.text})
        except:
            self.template_args['options'].append({'text': item.optionValue.text, 'value': item.optionValue.text})

    def get_options(self, item):
        pass

    def set_info(self, item):
        q_info = {}
        q_info['text'] = item.text
        try:
            q_info['cssClass'] = item.attrib['cssClass']
        except:
            q_info['cssClass'] = ''
        self.question_objects.append(q_info)

    def set_restrictions(self, item):
        for rule in item.getchildren():
            parameters = {}
            for p in rule.getchildren():
                parameters[p.attrib['use']] = p.text
            self.restrictions[rule.attrib['name']] = parameters

    def set_variable(self, item):
        """Sets the variable data type.  Variable name has already been set."""
        try:
            for dt in item.dataType.getchildren():
                self.data_type['type'] = dt.tag.replace('{http://www.mrc-epid.cam.ac.uk/schema/common/epi}', '')
                for child in dt.getchildren():
                    self.data_type[child.tag.replace('{http://www.mrc-epid.cam.ac.uk/schema/common/epi}', '')] = child.text
        except:
            pass

# Tod dos:
# 1. set table and shownumber on the QuestionGroup object, they come from
# the renderingHints.
# 2. Is there anything that can be rendered entirely by a template to string
# that doesn't have any data...  First sections etc.  Does it help?


class ImportQuestionGroup(MethodMixin):
    def __init__(self, question_group_object, app_object, section_object):
        self.app_object = app_object
        self.section = section_object
        self.question_group_objects = []
        self.title = question_group_object.title
        self.position = question_group_object.attrib['position']
        self.rendering_hints = {}
        self.build_question_group(question_group_object)
        self.info = []

    def build_question_group(self, question_group_object):
        for item in question_group_object.getchildren():
            self.tag_type(item.tag)(item)

    def set_info(self, item):
        qg_info = {}
        qg_info['text'] = item.text
        try:
            qg_info['cssClass'] = item.attrib['cssClass']
        except:
            qg_info['cssClass'] = ''
        self.question_group_objects.append(qg_info)

    def set_text_node(self, item):
        text_node = Bunch()
        text_node.rendering_hints = {}
        try:
            text_node['id'] = item.attrib['ID']
        except:
            text_node['id'] = None
        text_node['position'] = item.attrib['position']
        try:
            text_node['text'] = item.info.text
        except:
            text_node['text'] = ''
        for rh in item.renderingHint:
            key = rh.rhType.text
            text_node.rendering_hints[key] = ''
            for rhdata in rh.rhData:
                text_node.rendering_hints[key] = text_node.rendering_hints[key] + ' ' + str(rhdata)
            text_node.rendering_hints[key] = text_node.rendering_hints[key].strip()
        self.question_group_objects.append(text_node)

    def set_question(self, item):
        question = ImportQuestion(item, self.app_object, self.section)
        self.question_group_objects.append(question)

    def get_question(self, question):
        for q in self.question_group_objects:
            if q.position == question:
                return q


class ImportSection(MethodMixin):
    def __init__(self, section_xml_object, app_object):
        self.app_object = app_object
        self.section_xml_object = section_xml_object
        self.title = section_xml_object.title
        self.position = section_xml_object.attrib['position']
        self.info = []
        self.api = {}
        self.question_groups = []
        self.errors = {}
        self.section_objects = []
        self.rendering_hints = {}
        self.build_section()
        print self.info

    def build_section(self):
        for item in self.section_xml_object.getchildren():
            self.tag_type(item.tag)(item)

    def set_info(self, item):
        section_info = {}
        section_info['text'] = item.text
        try:
            section_info['cssClass'] = item.attrib['cssClass']
        except:
            section_info['cssClass'] = ''
        self.info.append(section_info)
        # self.section_objects.append(section_info)

    def set_question_group(self, item):
        question_group = ImportQuestionGroup(item, self.app_object, self)
        self.question_groups.append(question_group)
        self.section_objects.append(question_group)

    def get_question_group(self, question_group):
        for qg in self.question_groups:
            if qg.position == question_group:
                return qg


class Application(object):
    def __init__(self, xml):
        self.name = ''
        self.xml = xml
        self.xml_object = objectify.fromstring(self.xml)
        self.author = self.xml_object.author
        self.version_number = self.xml_object.versionNumber
        self.version_date = self.xml_object.versionDate
        self.title = self.xml_object.title
        self.studyname = self.xml_object.studyName
        self.sections = self.get_sections()
        self.rendering_hints = {}
        self.info = []

    def tidy(self, data):
        for k in data.keys():
            if isinstance(data[k], datetime.date):
                data[k] = str(data[k])

    def get_table_name(self, section_number):
        return self.mapping[int(section_number)]

    def get_section(self, section_number):
        return deepcopy(self.sections[str(section_number)])

    def get_sections(self):
        sections = {}
        for section in self.xml_object.section:
            sections[section.attrib['position']] = ImportSection(section, self)
        return sections

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
                        if isinstance(qgo, ImportQuestion):
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
        if isinstance(obj, ImportQuestion):
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
            if isinstance(qo, ImportQuestion):
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


app = Application(xml_string)

app.import_questionnaire()


if QUESTIONNAIRE_MODEL:
    d = BASE_DIR + '/' + APP_NAME
    if not os.path.exists(d):
        os.mkdir(APP_NAME)
    app.build_app(APP_NAME)

    
