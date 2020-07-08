from django.db import models


class Node(models.Model):
    id = models.CharField(max_length=1000)
    provider_domain = models.CharField(max_length=1000, primary_key=True)