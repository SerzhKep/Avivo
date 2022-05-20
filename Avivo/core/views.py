from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.urls import reverse

from .forms import LoginForm, SignupForm, UdateProfileForm


MAIN_PAGE_URL = '/'

class LoginView(LoginView):
    template_name = 'core/login.html'
    form_class = LoginForm
    next_page = MAIN_PAGE_URL


class SignUpView(View):
    template_name = 'core/signup.html'
    form_class = SignupForm

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(date=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)


@login_required
def logout_view(request):
    logout(request)
    return redirect(MAIN_PAGE_URL)