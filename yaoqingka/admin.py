# -*- coding:utf-8 -*-
from django.contrib import admin

# Register your models here.
# -*- coding:utf-8 -*-
from django.contrib import admin

# Register your models here.
from yaoqingka.models import InviteCard, Template_wish


class InviteCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_card_image4cms', 'word_postion','word_color','bg_color',
                    'title_color', 'can_show', 'order')
    list_filter = ('can_show', )
    search_fields = ('title', 'content', 'addressor', 'recipient')

    def save_model(self, request, obj, form, change):
        # if getattr(obj, 'author', None) is None:
        if change is False:
            obj.author = request.user
        obj.save()
class Template_wishAdmin(admin.ModelAdmin):
    list_display = ('id', 'details','created_at' , 'updated_at')
    search_fields = ('details',)

admin.site.register(InviteCard, InviteCardAdmin)
admin.site.register(Template_wish, Template_wishAdmin)