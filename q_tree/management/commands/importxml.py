from django.core.management.base import BaseCommand, CommandError
from xml_objectifier import objectifier
from bunch import Bunch
from q_tree.models import *


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
                                tn_data.title = qgo.text.strip()
                                if tn_data.title == '':
                                    tn_date.title = 'no title'
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


class Command(BaseCommand):
    args = '<xml_path app_name>'
    help = 'imports app models'

    def handle(self, *args, **options):
        app = ImportApplication(args[1], args[0])
        app.import_questionnaire()
