from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from polymorphic_tree.admin import PolymorphicMPTTParentModelAdmin, PolymorphicMPTTChildModelAdmin
from q_tree import models
from django.forms.models import model_to_dict


# The common admin functionality for all derived models:
def copy_paste(modeladmin, request, queryset):
    for q in queryset:
        old_id = q.id
        item = models.BaseTreeNode.copy_objects.get_subclass(pk=old_id)
        new_object = model_to_dict(item)
        new_object.pop('id')
        parent_id = new_object['parent']
        if parent_id:
            parent = models.BaseTreeNode.objects.get(pk=parent_id)
            new_object['parent'] = parent
        try:
            new_object.pop('basetreenode_ptr')
        except:
            pass
        if isinstance(item, models.Questionnaire):
            new_q = models.Questionnaire(**new_object)
            new_q.save()
        elif isinstance(item, models.Section):
            new_s = models.Section(**new_object)
            new_s.save()
        elif isinstance(item, models.QuestionGroup):
            new_qg = models.QuestionGroup(**new_object)
            new_qg.save()
        elif isinstance(item, models.Question):
            new_q = models.Question(**new_object)
            new_q.save()
        elif isinstance(item, models.TextNode):
            new_tn = models.TextNode(**new_object)
            new_tn.save()



class XMLPropertyInline(admin.TabularInline):
    model = models.XMLProperty
    fields = ('key', 'value')
    extra = 0
    
class InfoPropertyInline(admin.TabularInline):
    model = models.InfoProperty
    fields = ('key', 'value', 'text')
    extra = 0
    
class OptionPropertyInline(admin.TabularInline):
    model = models.OptionProperty
    fields = ('position', 'value', 'text')
    extra = 0


class BaseChildAdmin(PolymorphicMPTTChildModelAdmin):
    inlines = [XMLPropertyInline, InfoPropertyInline, OptionPropertyInline, ]
    GENERAL_FIELDSET = (None, {
        'fields': ('parent', 'title'),
    })

    actions = [copy_paste,]

    base_model = models.BaseTreeNode
    base_fieldsets = (
        GENERAL_FIELDSET,
    )


# Optionally some custom admin code

class TextNodeAdmin(BaseChildAdmin):
    pass


# Create the parent admin that combines it all:

class TreeNodeParentAdmin(PolymorphicMPTTParentModelAdmin):
    base_model = models.BaseTreeNode
    child_models = (
        (models.Questionnaire, BaseChildAdmin),
        #(models.TextNode, TextNodeAdmin),  # custom admin allows custom edit/delete view.
        (models.Section, BaseChildAdmin),
        (models.TextNode, BaseChildAdmin),
        (models.QuestionGroup, BaseChildAdmin),
        (models.Question, BaseChildAdmin),
        (models.ExternalProgram, BaseChildAdmin),
    )

    actions = [copy_paste,]

    list_display = ('title', 'actions_column',)

    class Media:
        css = {
            'all': ('admin/treenode/admin.css',)
        }



admin.site.register(models.BaseTreeNode, TreeNodeParentAdmin)


    
