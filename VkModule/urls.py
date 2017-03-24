from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', main_page, name='index'),
    url(r'^group_add$', group_add, name='group_add'),
    url(r'^add$', add_group, name='add_group'),
    url(r'^(?P<group_id>(\w+))$', group_info, name='group_info'),
    url(r'^(?P<group_id>(\w+))/delete$', delete_group, name='delete_group'),
    url(r'^(?P<group_id>(\w+))/change$', fix_change, name='change_group'),
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
]
