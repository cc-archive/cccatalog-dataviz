from django.db import models


class Node(models.Model):
    id = models.CharField(max_length=1000)
    # Index will either have provider_domain or id if it's not available
    index = models.CharField(max_length=1000, primary_key=True)