from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView, ModelFormMixin

from zad.forms import AuthForm
from .models import *
from django.contrib.auth.base_user import BaseUserManager
import datetime as idt
from .utils import password_generator

from django.core.urlresolvers import reverse


def index(request):
    info = 'info'
    return render(request, 'zad/index.html', {'info': info})


def home(request):
    agent = request.META['HTTP_USER_AGENT']
    print(agent)
    customerUrls = CustomerUrl.objects.all()
    customerFiles = CustomerFile.objects.all()
    context = {
        "customerUrls": customerUrls,
        "customerFiles": customerFiles,
    }

    return render(request, 'zad/home.html', context)


def upload_info(request, id):

    instance = get_object_or_404(CustomerUrl, pk=id)
    # instance = get_object_or_404(CustomerFile, pk=id)
    context = {
        "instance_password": instance.password,
        "instance_app_url": instance.get_absolute_url(),
    }

    return render(request, 'zad/info.html', context)


def upload_info_file(request, id):

    # instance = get_object_or_404(CustomerUrl, pk=id)
    instance = get_object_or_404(CustomerFile, pk=id)
    context = {
        "instance_password": instance.password,
        "instance_app_url": instance.get_absolute_url(),
    }

    return render(request, 'zad/info.html', context)


class AddUrl(CreateView):
    model = CustomerUrl
    fields = ['url']
    success_url = '/zad/home'

    def form_valid(self, form):
        form.instance.password = password_generator()
        self.object = form.save()
        print('ok valid')
        return super(ModelFormMixin, self).form_valid(form)  # doczytac o co sie rozchodzi i jak dzialaje te metody

    def get_success_url(self):
        print('ok success')
        return reverse('zad:upload_info', args=(self.object.id,))


class AddFile(CreateView):
    model = CustomerFile
    fields = ['file']
    success_url = '/zad/home'

    def form_valid(self, form):
        form.instance.password = password_generator()
        self.object = form.save()
        return super(ModelFormMixin, self).form_valid(form)  # doczytac o co sie rozchodzi i jak dzialaje te metody

    def get_success_url(self):
        return reverse('zad:upload_info_file', args=(self.object.id,))

        # def form_valid(self, form):
        #     form.instance.password = BaseUserManager().make_random_password()
        #     print(form.instance.password)
        #     form.save()
        #     return redirect('zad:home')


class ActionFile(FormView):
    template_name = 'zad/file_action.html'
    form_class = AuthForm
    success_url = '/zad/home'

    def form_valid(self, form):
        id = self.kwargs['id']
        password = form.cleaned_data['password']
        instance = get_object_or_404(CustomerFile, pk=id)

        if password == instance.password:

            update_counter(instance)

            if fresh_checker(instance):
                instance_file = instance.file
                filename = instance_file.file.name.split('/')[-1]
                response = HttpResponse(instance_file.file, content_type='text/plain')
                response['Content-Disposition'] = 'attachment; filename=%s' % filename
                return response
            else:
                return redirect('zad:home') # dorzucic info ze niema juz zasobu, moze w innej metodzie i URL
        else:
            return redirect(instance.get_absolute_url())


class ActionUrl(FormView):
    template_name = 'zad/url_action.html'
    form_class = AuthForm
    success_url = '/zad/home'

    def form_valid(self, form):
        id = self.kwargs['id']
        password = form.cleaned_data['password']
        instance = get_object_or_404(CustomerUrl, pk=id)
        instance_url = instance.url
        if password == instance.password:
            update_counter(instance)
            if fresh_checker(instance):
                return redirect(instance_url)
            else:
                return redirect('zad:home')
        else:
            return redirect(instance.get_absolute_url())


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('zad:home')
    else:
        form = UserCreationForm()
    return render(request, 'zad/signup.html', {'form': form})


def update_counter(instance):
    instance.counter = instance.counter + 1
    instance.save()


def fresh_checker(instance):
    instance_date = instance.date.replace(tzinfo=None)
    delta = idt.datetime.now() - idt.timedelta(hours=24)
    print(delta)
    if instance_date > delta:
        return True
    else:
        instance.delete()
        return False

