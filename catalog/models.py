from django.db import models

class Pet(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    description = models.TextField()
    image_url = models.URLField(max_length=500, blank=True, null=True)
    image_file = models.ImageField(upload_to='pets/', blank=True, null=True)
    is_adopted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
