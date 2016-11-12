from django.forms import ModelForm

from VkModule.models import GroupInfo


class GroupForm(ModelForm):
    class Meta:
        model = GroupInfo
        fields = ["group_id"]
