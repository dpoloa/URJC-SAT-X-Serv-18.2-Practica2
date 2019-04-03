from django.db import models


class NewURL(models.Model):
    URL_long = models.CharField(max_length=1024)
    URL_short = models.CharField(max_length=256)
