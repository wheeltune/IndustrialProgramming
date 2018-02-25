from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import ToDo
from .forms import AddFrom

from dateutil.parser import parse

def index(request):    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        addForm = AddFrom(request.POST)
        # check whether it's valid:
        # if addForm.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
        if addForm.is_valid():
            content = addForm.cleaned_data['content']
            deadline = addForm.cleaned_data['deadline']
            ToDo.objects.create(content=content, deadline=deadline)

            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        addForm = AddFrom()

    list = ToDo.objects.all()
    context = {'list': list, 'addForm': addForm}

    return render(request, 'list/index.html', context)