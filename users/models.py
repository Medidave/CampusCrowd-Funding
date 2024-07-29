from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Profile(models.Model):
    CATEGORY = (
        ('student', 'Student'),
        ('investor', 'Investor'),
        ('faculty', 'Faculty')
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='profile')
    profile_image = models.ImageField(null=True, blank=True, upload_to='CampusCrowd/profiles/', default="profiles/user-default.png")
    about_you = models.TextField(blank=True, null=True)
    reference_number = models.IntegerField(blank=True, null=True)
    programme_of_study = models.CharField(max_length=250, blank=True, null=True)
    name_of_institution = models.CharField(max_length=250, blank=True, null=True)
    abbreviation_of_institution = models.CharField(max_length=250, blank=True, null=True)
    college_name = models.CharField(max_length=250, blank=True, null=True)
    category = models.CharField(max_length=25, choices=CATEGORY, default='Student')
    contact = models.IntegerField(null=True, blank=True)
    linkedIn_url = models.CharField(max_length=300, blank=True, null=True)
    website_url = models.CharField(max_length=250, blank=True, null=True)
    stars = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return str(self.user.first_name + " " + self.user.last_name)
    
    class Meta:
        ordering = ['-created']
        
        
        
class Project(models.Model):
    project_owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=250, blank=True)
    brief_description = models.CharField(max_length=500)
    about_project = models.TextField(null=True, blank=True)
    project_image = models.ImageField(upload_to='CampusCrowd/project_images/')
    project_target_amount = models.IntegerField(null=True, blank=True)
    target_funding_period_in_days = models.IntegerField(null=True, blank=True)
    amount_raised = models.IntegerField(default=0)
    project_short_demo_video = models.FileField(null=True, blank=True, upload_to='CampusCrowd/project_videos/')
    project_stars = models.IntegerField(default=0)
    has_update = models.BooleanField(default=False)
    has_details = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return str(self.project_title)
    
    class Meta:
        ordering = ['-created']
        

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user.first_name + " " + self.user.last_name)

    class Meta:
        unique_together = ('user', 'project')


class ProjectUpdate(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=350)
    update = models.TextField()
    update_number = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return str(self.title)
    
    class Meta:
        ordering = ['-created']
    

class ProjectDetail(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    problem_statment = models.TextField(null=True, blank=True,)
    proposed_solution = models.TextField(null=True, blank=True,)
    market = models.TextField(null=True, blank=True,)
    statistical_image = models.ImageField(upload_to='CampusCrowd/project_images/')
    competition = models.TextField(null=True, blank=True,)
    Why_you = models.TextField(null=True, blank=True,)
    financing = models.TextField(null=True, blank=True,)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return str(self.project.project_title)
    