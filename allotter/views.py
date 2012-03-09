from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.http import Http404

from allotter.models import Profile, Option, Exam
from allotter.forms import RegistrationForm, UserLoginForm#, ApplicationForm

from settings import URL_ROOT


def user_register(request):
    """ Register a new user.
    Create a user and corresponding profile and store roll_number also."""

    user = request.user
    if user.is_authenticated():
        return redirect("/allotter/")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            u_name, pwd = form.save_data()

            new_user = authenticate(username = u_name, password = pwd)
            login(request, new_user)
            return redirect("/allotter/")
                
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
        return redirect("/allotter/")

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            login(request, user)
            return redirect("/allotter/")
        else:
            context = {"form": form}
            return render_to_response('allotter/login.html', context,
                        context_instance=RequestContext(request))
    else:
        form = UserLoginForm()
        context = {"form": form}
        return render_to_response('allotter/login.html', context,
                                     context_instance=RequestContext(request))

@login_required
def apply(request):
    user = request.user
    if not(user.is_authenticated()):
        return redirect('/allotter/login/')
    user_profile = user.get_profile()
    subject = user_profile.exam_code
    options_available = Option.objects.filter(exam__exam_name=subject).distinct()
    #form = ApplicationForm(user)
    context = {'user': user, 'subject': subject,
                'options' : options_available}
    ci = RequestContext(request)            
    return render_to_response('allotter/apply.html', context,
                            context_instance=ci)

def submit(request):
	pass

def quit(request):
	pass
        
def user_logout(request):
    logout(request)
    return redirect ('/allotter/')
