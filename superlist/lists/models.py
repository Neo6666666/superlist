from django.db import models


class Item(models.Model):
    '''List item'''
    text = models.TextField(default='')
