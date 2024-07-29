from django import forms
from .models import Reply, Message


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply']


    def __init__(self, *args, **kwargs):
           super(ReplyForm, self).__init__(*args, **kwargs)
           for name, field in self.fields.items():
               field.widget.attrs.update({'class': 'input'})



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']


    def __init__(self, *args, **kwargs):
           super(MessageForm, self).__init__(*args, **kwargs)
           for name, field in self.fields.items():
               field.widget.attrs.update({'class': 'input'})