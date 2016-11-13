# coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect as redirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
import vk
from datetime import datetime

from VkModule.forms import GroupForm
from VkModule.models import GroupInfo, ChangeGroup


def main_page(request):
    groups = GroupInfo.objects.all()
    f = GroupForm()
    if groups.exists():
        return render(request, "VkModule/groups.html", {"groups": groups, "f": f})
    else:
        return render(request, "VkModule/empty.html", {"f": f})


def add_group(request):
    if request.method == "GET":
        return redirect(reverse("VkModule:index"))
    elif request.method == "POST":
        f = GroupForm(request.POST)
        users = set_new_users(request.POST['group_id'])
        group = GroupInfo()
        group.users = str(users)
        if f.is_valid():
            group.group_id = f.cleaned_data["group_id"]
            session = vk.Session()
            api = vk.API(session)
            name = api.groups.getById(group_id=request.POST['group_id'])
            name = name[0]
            name = name[u'name']
            group.group_name = name
            group.save()
            return redirect(reverse("VkModule:group_info", args=(group.group_id,)))
    else:
        return HttpResponse("405")
    return 0


def delete_group(request, group_id):
    if request.method == "POST":
        groups = GroupInfo.objects.filter(group_id=group_id)
        group = groups[0]
        changes = ChangeGroup.objects.filter(group=group)
        changes.delete()
        group.delete()
    return redirect(reverse("VkModule:index"))


def group_info(request, group_id):
    groups = GroupInfo.objects.filter(group_id=group_id)
    group = groups[0]
    changes = ChangeGroup.objects.filter(group=group)
    for change in changes:
        change.delete_persons = eval(change.delete_persons)
        change.new_persons = eval(change.new_persons)
    return render(request, "VkModule/group_info.html", {"changes": changes, "group": group})


def fix_change(request, group_id):
    if request.method == "GET":
        return redirect(reverse("VkModule:index"))
    elif request.method == "POST":
        groups = GroupInfo.objects.filter(group_id=group_id)
        group = groups[0]
        users = group.users
        new_users = set_new_users(group_id)
        change = ChangeGroup()
        change.group = group
        del_persons = change.delete_persons = get_diff(eval(users), new_users)
        new_persons = change.new_persons = get_diff(new_users, eval(users))
        first = int(len(del_persons)) > 0
        second = int(len(new_persons)) > 0
        if first | second:
            change.date = datetime.today().date()
            change.save()
            users1 = str(new_users)
            group.users = users1
            group.save()
        return redirect(reverse("VkModule:group_info", args=(group_id,)))


def set_new_users(group_id):
    session = vk.Session()
    api = vk.API(session)
    members = api.groups.getMembers(group_id=group_id)
    count = int(members[u'count'])
    users = set(members[u'users'])
    number = 1000
    while count - number > 0:
        members = api.groups.getMembers(group_id=group_id, offset=number)
        users.update(set(members[u'users']))
        number += 1000
    return users


def get_diff(users, diff_set):
    return users.difference(diff_set)

# Create your views here.
