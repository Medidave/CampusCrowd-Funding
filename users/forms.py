from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile, Project, ProjectUpdate
from django.forms.widgets import CheckboxSelectMultiple, RadioSelect



class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    # username = forms.CharField(max_length=30, label='Username')


    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        # user.username = self.cleaned_data['username']
        user.save()
        return user
    
    
CATEGORY = (
    ('student', 'Student'),
    ('investor', 'Investor'),
    ('faculty', 'Faculty')
)

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        date_0f_birth = forms.DateField(widget=forms.SelectDateWidget)
        fields = ['profile_image', 'about_you', 'reference_number', 'programme_of_study', 'name_of_institution', 'abbreviation_of_institution', 'category', 'contact', 'linkedIn_url', 'website_url']
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields["category"].widget = RadioSelect(choices=CATEGORY)


        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
            
            
class ProjectForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = ['project_title', 'brief_description', 'about_project', 'project_image', 'project_target_amount', 'target_funding_period_in_days', 'project_short_demo_video']
        
        def __init__(self, *args, **kwargs):
            super(ProjectForm, self).__init__(*args, **kwargs)

            for name, field in self.fields.items():
                field.widget.attrs.update({'class': 'input'})
                
