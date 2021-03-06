from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', main_page, name='index'),
    url(r'^group_add$', group_add, name='group_add'),
    url(r'^add$', add_group, name='add_group'),
    url(r'^(?P<group_id>([a-zA-Z0-9\\._-]+))$', group_info, name='group_info'),
    url(r'^(?P<group_id>([a-zA-Z0-9\\._-]+))/delete$', delete_group, name='delete_group'),
    url(r'^(?P<group_id>([a-zA-Z0-9\\._-]+))/change$', fix_change, name='change_group'),
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^remove_persons/', get_remove_persons, name='remove_persons'),
    url(r'^remove_person/', remove_person, name='remove_person'),
]
