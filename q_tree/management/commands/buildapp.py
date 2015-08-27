from django.core.management.base import BaseCommand, CommandError
from q_tree.models import *
from xml_objectifier import objectifier
from django.conf import settings
import os

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


class ApplicationBuilder(objectifier.Application):
    
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
            if isinstance(qo, objectifier.Question):
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
        with open(app_name+'/models.py', 'w') as f:
            f.write(model_template % (app_name.capitalize(), choices, fields))
        self.build_admin(app_name)

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
        with open(app_name+'/admin.py', 'w') as f:
            f.write(admin_template % (app_name.capitalize(), app_name.capitalize(), app_name.capitalize(), app_name.capitalize()))


class Command(BaseCommand):
    args = '<xml_path app_name>'
    help = 'builds an app'

    def handle(self, *args, **options):
        app = ApplicationBuilder(args[1], args[0])
        d = settings.BASE_DIR + '/' + args[1]
        if not os.path.exists(d):
            os.mkdir(args[1])
        app.build_app(args[1])
