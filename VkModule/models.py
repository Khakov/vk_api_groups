# coding: utf-8
import datetime
from django.db import models
from django.utils.timezone import now


class GroupInfo(models.Model):
    class Meta():
        db_table = 'groups'

    group_id = models.CharField(max_length=100)
    group_name = models.TextField(default="No name")
    comment = models.TextField(default="-")
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

# Create your models here.
