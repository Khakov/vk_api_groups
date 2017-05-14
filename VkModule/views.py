# coding=utf-8
from __future__ import print_function

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect as redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render
from datetime import datetime, timedelta

from django.template.context_processors import csrf
from django.utils import timezone

from VkModule.forms import GroupForm, RemovePersonForm
from VkModule.models import ChangeGroup, GroupInfo, RemovePerson
from VkModule.vk_api_methods import Changs, get_diff, get_user_id_by_unformat_string, set_new_users, get_group_name

def exception_decorate(func):
    def decorate(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            back = "/"
            if len(args) > 1:
                back += args[1]
            return render(args[0], "VkModule/error.html", {"back": back})

@login_required(login_url=reverse_lazy("VkModule:login"))
def main_page(request):
    # groups = GroupInfo.objects.all()
    current_user = request.user
    groups = GroupInfo.objects.filter(user=current_user)
    if groups.exists():
        return render(request, "VkModule/groups.html", {"groups": groups})
    else:
        f = GroupForm()
        return render(request, "VkModule/empty.html", {"f": f})


@login_required(login_url=reverse_lazy("VkModule:login"))
def group_add(request):
    f = GroupForm()
    return render(request, "VkModule/empty.html", {"f": f, "back": '1'})


@login_required(login_url=reverse_lazy("VkModule:login"))
def add_group(request):
    try:
        if request.method == "GET":
            return redirect(reverse("VkModule:index"))
        elif request.method == "POST":
            f = GroupForm(request.POST)
            if GroupInfo.objects.filter(group_id=request.POST['group_id']).exists():
                return render(request, "VkModule/empty.html", {"f": f, "back": '1', "error": "1"})
            else:
                users = set_new_users(request.POST['group_id'])
                group = GroupInfo()
                group.users = str(users)
                if f.is_valid():
                    group.group_id = f.cleaned_data["group_id"]
                    group.comment = f.cleaned_data["comment"]
                    group.group_name = get_group_name(request.POST['group_id'])
                    group.user = request.user
                    group.save()
                    return redirect(reverse("VkModule:group_info", args=(group.group_id,)))
        else:
            return HttpResponse("405")
        return 0
    except Exception:
        return render(request, "VkModule/error.html", {"back": '/'})


@login_required(login_url=reverse_lazy("VkModule:login"))
def delete_group(request, group_id):
    try:
        groups = GroupInfo.objects.filter(group_id=group_id)
        if request.user == groups[0].user:
            if request.method == "POST":
                group = groups[0]
                changes = ChangeGroup.objects.filter(group=group)
                changes.delete()
                group.delete()
            return redirect(reverse("VkModule:index"))
        else:
            return redirect(reverse("VkModule:index"))
    except Exception:
        back = '/' + group_id
        return render(request, "VkModule/error.html", {"back": back})


@login_required(login_url=reverse_lazy("VkModule:login"))
def group_info(request, group_id):
    try:
        groups = GroupInfo.objects.filter(group_id=group_id)
        if request.user == groups[0].user:
            group = groups[0]
            changes = ChangeGroup.objects.filter(group=group).order_by("-date")
            if (RemovePerson.objects.exists()):
                delete_persons = set()
                for person in RemovePerson.objects.all():
                    delete_persons.add(int(person.remove_person.encode('utf-8')))
                print(delete_persons)
            else:
                delete_persons = set('1')
            changses = []
            for change in changes:
                changs = Changs()
                changs.delete_persons = (eval(change.delete_persons)).difference(delete_persons)
                changs.delete_persons_red = (eval(change.delete_persons)).intersection(delete_persons)
                changs.new_persons = (eval(change.new_persons)).difference(delete_persons)
                changs.new_persons_red = (eval(change.new_persons)).intersection(delete_persons)
                changs.date = change.date
                changses.append(changs)
            return render(request, "VkModule/group_info.html", {"changes": changses, "group": group})
        else:
            return redirect(reverse("VkModule:index"))
    except Exception:
        return render(request, "VkModule/error.html", {"back": '/'})


@login_required(login_url=reverse_lazy("VkModule:login"))
def fix_change(request, group_id):
    try:
        if request.user == GroupInfo.objects.get(group_id=group_id).user:
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
                time = request.POST.get("time", "")
                if time == '':
                    datetime.today().date()
                time = datetime.fromtimestamp(float(time) / 1000.0)
                time = timezone.make_aware(time, timezone.get_current_timezone())
                print(time)
                if first | second:
                    changes = ChangeGroup.objects.filter(date__lte=time - timedelta(days=3))
                    if changes != None:
                        changes.delete()
                    changes = ChangeGroup.objects.filter(date=time - timedelta(days=1))
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
                        ch.date = time - timedelta(days=1)
                        ch.save()
                    users1 = str(new_users)
                    group.users = users1
                    group.save()
                    change.date = time
                    change.save()
                return redirect(reverse("VkModule:group_info", args=(group_id,)))
            else:
                return redirect(reverse("VkModule:index"))
    except Exception as e:
        print(e.message)
        back = '/' + group_id
        return render(request, "VkModule/error.html", {"back": back})


def login(request):
    if request.user.is_authenticated():
        return redirect(reverse("VkModule:index"))
    if request.method == "GET":
        context = {}
        if "next" in request.GET:
            context["next"] = "?next=" + request.GET["next"]
        return render(request, "VkModule/login.html", context)
    elif request.method == "POST":
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        re = request.POST.get('remember_me')
        if user is not None:
            auth_login(request, user)
            if "next" in request.GET:
                h = redirect(request.GET["next"])
                if re != None:
                    h.set_cookie(key="remember", value=user.username, max_age=24 * 60 * 60)
                return h
            else:
                h = redirect(reverse("VkModule:index"))
                if re != None:
                    h.set_cookie(key="remember", value=user.username, max_age=24 * 60 * 60)
                return h
        else:
            args = {}
            args.update(csrf(request))
            args['login_error'] = "No this user"
            args['login'] = request.POST["username"]
            return render(request, "VkModule/login.html", args)
    else:
        return HttpResponse("405")


@login_required()
def logout(request):
    auth_logout(request)
    return redirect(reverse("VkModule:login"))


@login_required(login_url=reverse_lazy("VkModule:login"))
def get_remove_persons(request):
    pass


@login_required(login_url=reverse_lazy("VkModule:login"))
def remove_person(request):
    try:
        if request.method == "GET":
            f = RemovePersonForm()
            return render(request, "VkModule/add_remove_person.html", {"f": f})
        elif request.method == "POST":
            f = RemovePersonForm(request.POST)
            if f.is_valid():
                remove_person_id = get_user_id_by_unformat_string(request.POST['remove_person'])
                if RemovePerson.objects.filter(remove_person=remove_person_id).exists():
                    return render(request, "VkModule/add_remove_person.html", {"f": f, "back": '/', "error": "1"})
                else:
                    remove_person = RemovePerson()
                    remove_person.remove_person = remove_person_id
                    remove_person.save()
                    f = RemovePersonForm()
                    return render(request, "VkModule/add_remove_person.html", {"f": f, "back": '/'})
            else:
                return render(request, "VkModule/add_remove_person.html", {"f": f})
        else:
            return HttpResponse("405")
    except Exception:
        return render(request, "VkModule/error.html", {"back": '/remove_person'})
