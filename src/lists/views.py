from django.shortcuts import render, redirect
from django.http import HttpResponse

from lists.models import Item, List


def home_page(request):
    """Домашняя страница"""
    # TODO Support multilists
    return render(request, 'lists/home.html')


def view_list(request, list_id):
    """Представление списка"""
    list_ = List.objects.get(id=list_id)
    return render(request, 'lists/list.html', context={'list': list_})


def new_list(request):
    """Представление нового списка"""
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')


def add_item(request, list_id):
    """Представление добавления нового элемента"""
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')
