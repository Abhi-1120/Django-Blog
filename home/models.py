from django.db import models


class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    content = models.TextField()
    timestamp = models.TimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name
