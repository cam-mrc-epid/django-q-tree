from django.db import models
from django.utils.translation import ugettext_lazy as _
from polymorphic_tree.models import PolymorphicMPTTModel, PolymorphicTreeForeignKey
from tinymce.models import HTMLField


class BaseTreeNode(PolymorphicMPTTModel):
    parent = PolymorphicTreeForeignKey('self', blank=True, null=True, related_name='children', verbose_name=_('parent'))
    title = models.CharField(_("Title"), max_length=200)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("Questionnaires")
        verbose_name_plural = _("Questionnaires")
    

class Questionnaire(BaseTreeNode):
    lang = models.CharField(max_length=50)
    css = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    study_name = models.CharField(max_length=50)
    version_number = models.CharField(max_length=50)
    version_date = models.CharField(blank=True, null=True, max_length=50)
    subtitle = models.CharField(blank=True, null=True, max_length=50)
    info = models.CharField(blank=True, null=True, max_length=50) # HTMLField would be good.
    # rendering_hints = 
    # lang
    q_id = models.CharField(blank=True, null=True, max_length=10)
    # css - css file to use.

    class Meta:
        verbose_name = _("Questionnaire")
        verbose_name_plural = _("Questionnaires")


class Section(BaseTreeNode):
    # info
    # video
    # rendering_hints
    header = HTMLField(blank=True, null=True)
    footer = HTMLField(blank=True, null=True)

    
    class Meta:
        verbose_name = _("Section")
        verbose_name_plural = _("Sections")


class QuestionGroup(BaseTreeNode):
    position = models.IntegerField()
    qg_id = models.CharField(max_length=10, blank=True, null=True)
    # info
    # video
    # rendering_hints
    header = HTMLField(blank=True, null=True)
    footer = HTMLField(blank=True, null=True)
    
    # could have qg have get_questions, get_text_nodes methods.
    
    class Meta:
        verbose_name = _("Question Group")
        verbose_name_plural = _("Question Groups")


class TextNode(BaseTreeNode):
    t_id = models.CharField(max_length=10, blank=True, null=True)
    position = models.IntegerField()
    # info
    # rendering_hints: could make this a choice?
    can_have_children = False
    
    def get_cname(self):
        return 'Text Node'
    
    class Meta:
        verbose_name = _("text Node")
        verbose_name_plural = _("Text Nodes")
    
class Question(BaseTreeNode):
    # info
    choices = ()
    var_name = models.CharField(max_length=20)
    # var_id 
    position = models.IntegerField()
    # show which allows a extra set of id'ed questions appear.
    # show adds to data-show attribute
    # hide, as above
    # enable, as above addes to data-enabled attribute
    # disable, etc. data-disable
    # choices = list of possibel answers for this question.
    # tooltips?
    # rendering_hints
    # restrictions - moved to model definition and form.
    # external_programs - djangui type thing?  
    # could add labels etc. that could be used more easily in templates than a text node.
    can_have_children = False
    
    def get_cname(self):
        return 'Question'
    
    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        

class XMLProperty(models.Model):
    choices = (
        (1, 'Rendering Hint:tdclass'),
        (2, 'Rendering Hint:qtype'),
        (3, 'Rendering Hint:endoftr'),
        (4, 'Rendering Hint:shownumber'),
        (5, 'Rendering Hint:table'),
        (6, 'Rendering Hint:size'),
        (7, 'search'),
    )
    node = models.ForeignKey(BaseTreeNode, blank=True, null=True)
    key = models.IntegerField(choices=choices, db_index=True)
    value = models.CharField(max_length=100, db_index=True)


class InfoProperty(models.Model):
    choices = (
        (1, 'Info:cssClass'),
    )
    node = models.ForeignKey(BaseTreeNode, blank=True, null=True)
    key = models.IntegerField(choices=choices, db_index=True)
    value = models.CharField(max_length=100, db_index=True)
    text = models.TextField(blank=True, null=True)


class OptionProperty(models.Model):
    node = models.ForeignKey(BaseTreeNode, blank=True, null=True)
    position = models.IntegerField(choices=choices, db_index=True)
    value = models.CharField(max_length=100, db_index=True)


class ExternalProgram(BaseTreeNode):
    position = models.IntegerField()
    
    can_have_children = False
