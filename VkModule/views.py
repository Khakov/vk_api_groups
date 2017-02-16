# coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect as redirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
import vk
from datetime import datetime, timedelta

from VkModule.forms import GroupForm
from VkModule.models import GroupInfo, ChangeGroup


def main_page(request):
    groups = GroupInfo.objects.all()
    if groups.exists():
        return render(request, "VkModule/groups.html", {"groups": groups})
    else:
        f = GroupForm()
        return render(request, "VkModule/empty.html", {"f": f})


def group_add(request):
    f = GroupForm()
    return render(request, "VkModule/empty.html", {"f": f, "back": '1'})


def add_group(request):
    try:
        if request.method == "GET":
            return redirect(reverse("VkModule:index"))
        elif request.method == "POST":
            f = GroupForm(request.POST)
            users = set_new_users(request.POST['group_id'])
            group = GroupInfo()
            group.users = str(users)
            if f.is_valid():
                group.group_id = f.cleaned_data["group_id"]
                group.comment = f.cleaned_data["comment"]
                group.group_name = get_group_name(request.POST['group_id'])
                group.save()
                return redirect(reverse("VkModule:group_info", args=(group.group_id,)))
        else:
            return HttpResponse("405")
        return 0
    except Exception:
        return render(request, "VkModule/error.html", {"back": '/'})


def get_group_name(id):
    session = vk.Session()
    api = vk.API(session)
    name = api.groups.getById(group_id=id)
    name = name[0]
    name = name[u'name']
    return name


def delete_group(request, group_id):
    try:
        if request.method == "POST":
            groups = GroupInfo.objects.filter(group_id=group_id)
            group = groups[0]
            changes = ChangeGroup.objects.filter(group=group).order_by("-date")
            changes.delete()
            group.delete()
        return redirect(reverse("VkModule:index"))
    except Exception:
        back = '/' + group_id
        return render(request, "VkModule/error.html", {"back": back})


def group_info(request, group_id):
    try:
        groups = GroupInfo.objects.filter(group_id=group_id)
        group = groups[0]
        changes = ChangeGroup.objects.filter(group=group).reverse()
        for change in changes:
            change.delete_persons = eval(change.delete_persons)
            change.new_persons = eval(change.new_persons)
        return render(request, "VkModule/group_info.html", {"changes": changes, "group": group})
    except Exception:
        return render(request, "VkModule/error.html", {"back": '/'})


def fix_change(request, group_id):
    try:
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
                changes = ChangeGroup.objects.filter(date__lte=datetime.today().date() - timedelta(days=2))
                if changes != None:
                    changes.delete()
                changes = ChangeGroup.objects.filter(date=datetime.today().date() - timedelta(days=1))
                if len(changes) > 2:
                    del_persons = eval(changes[0].delete_persons)
                    new_persons = eval(changes[0].new_persons)
                    for ch in changes:
                        del_persons.update(eval(ch.delete_persons))
                        new_persons.update(eval(ch.new_persons))
                    changes.delete()
                    ch = ChangeGroup()
                    ch.group = group
                    ch.delete_persons = get_diff(del_persons, new_persons)
                    ch.new_persons = get_diff(new_persons, del_persons)
                    ch.date = datetime.today().date() - timedelta(days=1)
                    ch.save()
                change.date = datetime.today().date()
                users1 = str(new_users)
                group.users = users1
                group.save()
                change.save()
            return redirect(reverse("VkModule:group_info", args=(group_id,)))
    except Exception:
        back = '/' + group_id


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
