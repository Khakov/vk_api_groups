from django.forms import ModelForm

from VkModule.models import GroupInfo


class GroupForm(ModelForm):
    class Meta:
        model = GroupInfo
        fields = ["group_id", "comment"]

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['group_id'].widget.attrs['class'] = 'input-group form-control'
        self.fields['comment'].widget.attrs['class'] = 'input-group form-control'
