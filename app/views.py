from django.shortcuts import render
from .forms import NameForm
from subprocess import call


def basic(request):
    if request.method == 'POST':
        return prediction(request)
    return render(request, 'index.html')


def prediction(request):
    form = NameForm(request.POST)
    id = form.data['prediction']
    call('python3 index.py ' + str(id), cwd='/home/ftlka/Documents/diploma/brute_classifier', shell=True)
    file = open('results.txt', 'r')
    results = file.read().split(' ')

    return render(request, 'prediction.html', {'ids': results})


