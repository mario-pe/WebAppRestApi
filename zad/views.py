from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView, ModelFormMixin

from zad.forms import AuthForm
from .models import *
from .utils import *


def index(request):
    info = 'info'
    return render(request, 'zad/index.html', {'info': info})

@login_required
def home(request):
    user_agent_support(request)
    customerUrls = CustomerUrl.objects.all()
    customerFiles = CustomerFile.objects.all()
    context = {
        "customerUrls": customerUrls,
        "customerFiles": customerFiles,
    }

    return render(request, 'zad/home.html', context)

@login_required
def upload_info(request, id):
    user_agent_support(request)
    instance = get_object_or_404(CustomerUrl, pk=id)
    context = {
        "instance_password": instance.password,
        "instance_app_url": instance.get_absolute_url(),
    }

    return render(request, 'zad/info.html', context)

@login_required
def upload_info_file(request, id):
    user_agent_support(request)
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
        user_agent_support(self.request)
        form.instance.password = password_generator()
        self.object = form.save()
        print('ok valid')
        return super(ModelFormMixin, self).form_valid(form)

    def form_invalid(self, form):
        user_agent_support(self.request)

    def get_success_url(self):
        print('ok success')
        return reverse('zad:upload_info', args=(self.object.id,))


class AddFile(CreateView):
    model = CustomerFile
    fields = ['file']
    success_url = '/zad/home'

    def form_valid(self, form):
        user_agent_support(self.request)
        form.instance.password = password_generator()
        self.object = form.save()
        return super(ModelFormMixin, self).form_valid(form)

    def form_invalid(self, form):
        user_agent_support(self.request)

    def get_success_url(self):
        return reverse('zad:upload_info_file', args=(self.object.id,))


class ActionFile(FormView):
    template_name = 'zad/file_action.html'
    form_class = AuthForm
    success_url = '/zad/home'

    def form_valid(self, form):
        user_agent_support(self.request)
        id = self.kwargs['id']
        password = form.cleaned_data['password']
        instance = get_object_or_404(CustomerFile, pk=id)

        if password == instance.password:
            update_counter(instance)
            update_archive_file(instance)
            instance_file = instance.file
            filename = instance_file.file.name.split('/')[-1]
            response = HttpResponse(instance_file.file, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            return response
        else:
            return redirect(instance.get_absolute_url())

    def form_invalid(self, form):
        user_agent_support(self.request)


class ActionUrl(FormView):
    template_name = 'zad/url_action.html'
    form_class = AuthForm
    success_url = '/zad/home'

    def form_valid(self, form):
        user_agent_support(self.request)
        id = self.kwargs['id']
        password = form.cleaned_data['password']
        instance = get_object_or_404(CustomerUrl, pk=id)
        instance_url = instance.url
        if password == instance.password:
            update_counter(instance)
            update_archive_url(instance)
        else:
            return redirect(instance.get_absolute_url())

    def form_invalid(self, form):
        user_agent_support(self.request)

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




