from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import NameForm


# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

# https://docs.djangoproject.com/en/2.1/topics/forms/


def get_name(request):
    if request.method == 'POST':
        print(request)
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

            # if a GET (or any other method) we'll create a blank form
        else:
            form = NameForm()

            return render(request, 'index.html', {'form': form})

