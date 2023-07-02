from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import AbvUser, SuperRubric, SubRubric, AdditionalImage, Bb
from .forms import SubRubricForm
# Register your models here.

class AbvUserAdmin(admin.ModelAdmin):
    list_display = ['id','username','first_name','last_name','email','is_staff','is_activated','send_messages']
    fields = ('id','username','first_name','last_name','email','is_staff','is_activated','send_messages')
    list_display_links = ('username',)
    search_fields = ('username',)
    search_help_text = 'Поиск по пользователям'
    list_editable = ('is_activated','send_messages',)

admin.site.register(AbvUser,AbvUserAdmin )

#Надрубрики + редактор подрубрик
class SubRubricInline(admin.TabularInline):
    model = SubRubric
class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ('super_rubric',)
    inlines = (SubRubricInline,)
admin.site.register(SuperRubric,SuperRubricAdmin )

#Подрубрики
class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm
admin.site.register(SubRubric,SubRubricAdmin )
#Редактирование объявлений

class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage
class BbAdmin(admin.ModelAdmin):
    list_display = ('rubric','title','content','price','contacts','get_html_photo','autor',)
    fields = (('rubric','autor',),'title','content','price','contacts','image','is_avtive')
    inlines = (AdditionalImageInline,)
    def get_html_photo(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=35>")
    get_html_photo.short_description = 'Фото'

admin.site.register(Bb,BbAdmin )