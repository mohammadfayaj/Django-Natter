from django.contrib import admin
from natter.models import GroupMessage, GroupRoom
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin
# Register your models here.

admin.site.register(GroupRoom)
admin.site.register(GroupMessage, DraggableMPTTAdmin, 
list_display = ('tree_actions','user','indented_title',),
list_filter = ['user','msg',]
)

