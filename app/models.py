from django.db import models

class Information(models.Model):
    full_name = models.CharField(max_length=100)
    dob = models.DateField(auto_now=False, auto_now_add=False)
    email = models.EmailField()
    phone = models.PositiveIntegerField()
    linkedIn = models.URLField()
    skypeId = models.URLField()
    drive_link = models.URLField(default="default is null")
    
    def __str__(self):
        return self.full_name
