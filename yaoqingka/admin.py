# -*- coding:utf-8 -*-
from django.contrib import admin

# Register your models here.
# -*- coding:utf-8 -*-
from django.contrib import admin

# Register your models here.
from yaoqingka.models import InviteCard

class InviteCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content','meeting_time', 'meeting_location', 'word_postion','word_color','bg_color',
                    'addressor', 'recipient', 'can_show', 'order', 'author', )
    list_filter = ('can_show', )
    search_fields = ('title', 'content', 'addressor', 'recipient')

    def save_model(self, request, obj, form, change):
        # if getattr(obj, 'author', None) is None:
        if change is False:
            obj.author = request.user
        obj.save()

admin.site.register(InviteCard, InviteCardAdmin)