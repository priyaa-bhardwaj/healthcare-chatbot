from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(models.Model):
    username=models.CharField(max_length=15)
    password=models.CharField(max_length=15)
    ph=models.CharField(max_length=15,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username
    
    
class Question(models.Model):
    user =models.ForeignKey(CustomUser,related_name='chat', on_delete=models.CASCADE)
    question=models.TextField()
    answer=models.TextField(blank=True,null=True)
    
    def __str__(self):
        return f"Question by {self.user.username}: {self.question[:50]}"
    
class Appointment(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    time=models.TimeField()
    date=models.DateField()
    description=models.TextField(blank=True)
    
    def __str__(self):
        return f"Appointment by {self.user.username} on {self.date} at {self.time}"