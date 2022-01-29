from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import *
from .models import *
from .utils import DataMixin


class Index(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = UserDataMeta.objects.all()[:5]
        return context

def login(request):
    if request.method == 'POST':
        form = LoginAccess(request.POST)
        if form.is_valid():
            try:
                return redirect('index')
            except:
                form.add.error(None, 'Error Invidalid Data')
    else:
        form = LoginAccess()
    return render(request, 'authconnection/login.html', {'form': form}, )

class generatepromo(LoginRequiredMixin ,DataMixin ,CreateView):
    form_class = Generate
    template_name = 'authconnection/generate.html'
    success_url = reverse_lazy('index')
    login_url = reverse_lazy ('login')
    #raise_exception = True
    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Generate Promo")
        return dict(list(context.items()) + list(c_def.items()))



class RegisterUser(DataMixin, CreateView):

    form_class = RegisterUserForm
    template_name = 'authconnection/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *,  object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Register")
        return dict(list(context.items()) + list(c_def.items()))



# def register(request):
#     if request.method == 'POST':
#         form = Register(request.POST)
#         if form.is_valid():
#             try:
#                 form.save()
#                 return redirect('index')
#             except:
#                 form.add.error(None, 'Error Invidalid Data')
#     else:
#         form = Register()
#     return render(request, 'authconnection/register.html', {'form': form},)

def pageNotFound(request, exceptions):
    return HttpResponseNotFound('Page not found 404')
