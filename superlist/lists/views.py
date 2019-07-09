from django.shortcuts import render, redirect
from django.http import HttpResponse

from lists.models import Item


def home_page(request):
    """Домашняя страница"""
    # TODO Support multilists
    return render(request, 'lists/home.html')


def view_list(request):
    """Представление списка"""
    items = Item.objects.all()
    return render(request, 'lists/list.html', context={'items': items})


def new_list(request):
    """Представление нового списка"""
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/new-list')