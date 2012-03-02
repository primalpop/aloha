from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import Http404

from allotter.models import Profile
from allotter.forms import RegistrationForm, UserLoginForm

from settings import URL_ROOT

def index(request):
    """The start page.
    """
    user = request.user
    if user.is_authenticated():
        return redirect("/allotter/hello/")

    return redirect("/allotter/login/")

def user_register(request):
    """ Register a new user.
    Create a user and corresponding profile and store roll_number also."""

    user = request.user
    if user.is_authenticated():
        return redirect("/allotter/hello/")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            u_name, pwd = form.save()

            new_user = authenticate(username = u_name, password = pwd)
            login(request, new_user)
            return redirect("/allotter/login/")
                
        else:
            return render_to_response('allotter/register.html',
                {'form':form},
                context_instance=RequestContext(request))
    else:
        form = RegistrationForm()
        return render_to_response('allotter/register.html',
                {'form':form},
                context_instance=RequestContext(request))

def user_login(request):
    """Take the credentials of the user and log the user in."""

    user = request.user
    if user.is_authenticated():
        return redirect("/allotter/hello/")

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            login(request, user)
            return redirect("/allotter/hello/")
        else:
            context = {"form": form}
            return render_to_response('allotter/login.html', context,
                        context_instance=RequestContext(request))
    else:
        form = UserLoginForm()
        context = {"form": form}
        return render_to_response('allotter/login.html', context,
                                     context_instance=RequestContext(request))

def hello(request):
    user = request.user
    context = {'user': user}
    ci = RequestContext(request)
    return render_to_response('allotter/hello.html', context, 
                                     context_instance=ci)

