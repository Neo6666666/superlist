from django.db import models


class List(models.Model):
    """Список дел"""
    pass


class Item(models.Model):
    """Элемент списка"""
    text = models.TextField(default='')
    list = models.ForeignKey(List, models.SET_NULL, null=True, blank=True)
