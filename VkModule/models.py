# coding: utf-8
import datetime
from django.db import models
from django.contrib.auth.models import User


class GroupInfo(models.Model):
    class Meta():
        db_table = 'groups'

    group_id = models.CharField(max_length=100)
    group_name = models.TextField(default="No name")
    comment = models.TextField(default="-")
    user = models.ForeignKey(User)
    users = models.TextField()

    def __unicode__(self):
        return "%s:%s" % (self.group_id, self.users)


class ChangeGroup(models.Model):
    class Meta():
        db_table = 'changes'

    delete_persons = models.TextField()
    new_persons = models.TextField()
    group = models.ForeignKey(GroupInfo)
    date = models.DateTimeField()

class RemovePerson(models.Model):
    class Meta():
        db_table = 'remove_persons'

    remove_person = models.CharField(max_length=100)
# Create your models here.
