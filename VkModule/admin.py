from django.contrib import admin

from VkModule.models import GroupInfo, ChangeGroup, RemovePerson

admin.site.register(GroupInfo)
admin.site.register(ChangeGroup)
admin.site.register(RemovePerson)
# Register your models here.
