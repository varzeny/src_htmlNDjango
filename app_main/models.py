from django.db import models

# Create your models here.

class Robot(models.Model):
    name=models.CharField(max_length=30)
    type=models.CharField(max_length=30,blank=True)
    image=models.ImageField(default='no-image-icon.png')
    ip=models.CharField(max_length=30,blank=True)
    port=models.IntegerField(blank=True)
    online=models.BooleanField(default=False)
    status=models.JSONField(blank=True,default=dict)
    task=models.CharField(max_length=100,blank=True,null=True)

    note=models.TextField(blank=True,null=True)


    def __str__(self):
        return f"[{self.pk}] {self.name}"
    


class Post(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.text