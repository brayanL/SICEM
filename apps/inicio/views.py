from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy


class NextUrlMixin(object):
    """ Allows to redirect a view to its correct success url. """
    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET.get('next')
        return reverse_lazy('index')


@login_required(login_url='/login')
def indexView(request):
    return render(request, "index.html")


class LoginView(NextUrlMixin, FormView):
    form_class = LoginForm
    template_name = 'login.html'
    # success_url = '/'

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password']
                            )

        if user is not None:
            if user.is_active:
                login(self.request, user)
        return super(LoginView, self).form_valid(form)


def LogOut(request):
    print('estamos bien')
    logout(request)
    return redirect('/')
