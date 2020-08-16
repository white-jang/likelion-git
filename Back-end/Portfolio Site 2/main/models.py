from django.db import models

# Create your models here.
class Content(models.Model):
    title = models.CharField(max_length=40)
    image = models.ImageField(upload_to='images/')
    link = models.TextField(null=True)
    content = models.TextField()

    def __str__(self):
            return self.title