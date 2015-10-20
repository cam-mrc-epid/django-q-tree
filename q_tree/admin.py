from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from polymorphic_tree.admin import PolymorphicMPTTParentModelAdmin, PolymorphicMPTTChildModelAdmin
from . import models


# The common admin functionality for all derived models:
def copy_paste(modeladmin, request, queryset):
    for q in queryset:
        q_new = q
        q_new.id = None
        q_new.save()


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


    