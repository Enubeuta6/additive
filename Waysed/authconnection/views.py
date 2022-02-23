from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, request
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, ListView
from django.contrib.auth.views import LoginView


from .forms import *
from .models import *
from .utils import DataMixin, AnonymousRequiredMixin


class Index(DataMixin ,TemplateView):
    model = UserDataMeta
    template_name = "authconnection/index.html"
    context_object_name = 'dbData'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = UserDataMeta.objects.all()[:5]
        return context


class Profile(LoginRequiredMixin, DataMixin, ListView):
        template_name = 'authconnection/profile.html'
        model = UserDataMeta

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            c_def = self.get_user_context(title="Profile")
            return dict(list(context.items()) + list(c_def.items()))


class LoginUser(AnonymousRequiredMixin ,DataMixin, LoginView):
        form_class = LoginUserForm
        template_name = 'authconnection/login.html'
        redirect_authenticated_user = 'index'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            c_def = self.get_user_context(title="Authorization")
            return dict(list(context.items()) + list(c_def.items()))

        def get_success_url(self):
            return reverse_lazy('index')




class generatepromo(LoginRequiredMixin ,DataMixin ,CreateView):
    model = PromoDataMeta
    form_class = Generate
    template_name = 'authconnection/generate.html'
    success_url = reverse_lazy('index')
    login_url = reverse_lazy ('login')


    #raise_exception = True
    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Generate Promo")
        return dict(list(context.items()) + list(c_def.items()))



def logout_user(request):
    logout(request)
    return redirect('login')


class RegisterUser(AnonymousRequiredMixin, DataMixin, CreateView):
        redirect_authenticated_user = 'index'
        form_class = RegisterUserForm
        template_name = 'authconnection/register.html'
        success_url = reverse_lazy('login')

        def get_context_data(self, *,  object_list=None,**kwargs):
            context = super().get_context_data(**kwargs)
            c_def = self.get_user_context(title="Register")
            return dict(list(context.items()) + list(c_def.items()))


        def form_valid(self, form):
            user = form.save()
            login(self.request, user)
            return redirect('index')


def pageNotFound(request, exceptions):
    return HttpResponseNotFound('Page not found 404')
