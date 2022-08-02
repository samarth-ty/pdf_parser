from django.db import models

class Information(models.Model):
    drive_link = models.URLField(default="default is null")
    
    def __str__(self):
        return self.full_name
