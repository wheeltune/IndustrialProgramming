from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import ToDo
from .forms import AddFrom, RemoveForm, MarkDoneForm

from dateutil.parser import parse

from datetime import datetime

def index(request):   
    if request.method == 'POST':
        add_form = AddFrom(request.POST)

        if add_form.is_valid():
            content = add_form.cleaned_data['content']
            deadline = add_form.cleaned_data['deadline']
            ToDo.objects.create(content=content, deadline=deadline)

            return HttpResponseRedirect('/')
    else:
        add_form = AddFrom()

    lists = []
    datas = []
    datas.append(("Активные", ToDo.objects.filter(deadline__gt=datetime.now(), is_done=False).order_by('deadline')))
    datas.append(("Просроченные", ToDo.objects.filter(deadline__lte=datetime.now(), is_done=False).order_by('deadline')))
    datas.append(("Завершенные", ToDo.objects.filter(is_done=True).order_by('deadline')))

    for title, data in datas:
        if len(data) > 0:
            remove_forms = []
            mark_done_forms = []
            for item in data:
                mark_done_forms.append(MarkDoneForm(initial={'id': item.id, 'is_done': item.is_done}))
                remove_forms.append(RemoveForm(initial={'id': item.id}))
            lists.append((title, zip(data, mark_done_forms, remove_forms)))

    context = {'lists': lists, 'addForm': add_form}

    return render(request, 'list/index.html', context)


def remove(request):
    if request.method == 'POST':
        remove_form = RemoveForm(request.POST)

        if remove_form.is_valid():
            id = remove_form.cleaned_data['id']
            instance = ToDo.objects.get(id=id)
            instance.delete()
    else:
        remove_form()

    return HttpResponseRedirect('/')

def markDone(request):
    if request.method == 'POST':
        mark_done_form = RemoveForm(request.POST)

        if mark_done_form.is_valid():
            print(mark_done_form.cleaned_data)
            id = mark_done_form.cleaned_data['id']
            is_done = request.POST.get('is_done') == 'on'
            instance = ToDo.objects.filter(id=id).update(is_done=is_done)
            
    return HttpResponseRedirect('/')