from django.db import models
from django.contrib.auth.models import User
import uuid
from users.models import Project



# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=30, decimal_places=2)
    email = models.EmailField()
    payer_name = models.CharField(max_length=250, null=True, blank=True)
    is_anonymous = models.BooleanField(default=False)
    reference = models.CharField(max_length=150, unique=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Payment for '{self.project.project_title}' - {self.status}"
    
    
# Create your models here.
class Suggestions(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        
    def __str__(self):
        return f"Suggestion for: {self.project.project_title}"
