from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.http import Http404

#TODO: Remove this if possible
from django.http import HttpResponseRedirect 
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from allotter.models import Profile, Option, Exam
from allotter.forms import UserLoginForm

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
                                     


def get_options(user):
    user_profile = user.get_profile()
    user_application = user_profile.application
    np = user_application.np #Number of Papers
    first_paper = user_application.first_paper #First Paper Name
    options_available_first = Option.objects.filter(exam__exam_name=first_paper).distinct() #Options for First paper
    if(np == 2):
        second_paper = user_application.second_paper
        options_available_second = Option.objects.filter(exam__exam_name=second_paper).distinct()
          
    options_available = list(set(options_available_first + options_available_second))
    

## Retrieves the user details from the database and passes it for generation
## of Application Template

##TODO: Display a single list of options for students who have taken two exams.

def get_details(user, error_message = ""):
    user_profile = user.get_profile()
    user_application = user_profile.application
    np = user_application.np #Number of Papers
    first_paper = user_application.first_paper #First Paper Name
    options_available_first = Option.objects.filter(exam__exam_name=first_paper).distinct() #Options for First paper
    oafl = len(options_available_first)  
    if np == 2: #If written two exams
        second_paper = user_application.second_paper
        options_available_second = Option.objects.filter(exam__exam_name=second_paper).distinct()
        oasl = len(options_available_second)
        context = {'user': user, 'first_paper': first_paper,
            'options_available_first' : options_available_first, 
            'second_paper': second_paper, 
            'options_available_second' : options_available_second,
            'np' : np,'oafl': oafl, 'oasl': oasl,
            'error_message': error_message}    
    else: #If written only one exam
        context = {'user': user, 'first_paper': first_paper,
            'options_available_first' : options_available_first,
            'oafl': oafl, 'np' : np, 'error_message' : error_message}     
    return context              
                                     
@login_required
def apply(request):
    user = request.user
    if not(user.is_authenticated()):
        return redirect('/allotter/login/')
    
    context = get_details(user) 
    ci = RequestContext(request)
              
    return render_to_response('allotter/apply.html', context,
        context_instance=ci)                         

##Logouts the user.

def user_logout(request):
    logout(request)
    return redirect ('/allotter/')

#TODO: Extensive Testing
                            
def submit(request, reg_no):
    user = get_object_or_404(User, username=reg_no)
    user_profile = user.get_profile()
    user_application = user_profile.application
    first_paper = user_application.first_paper #First Paper Name
    options_available_first = Option.objects.filter(exam__exam_name=first_paper).distinct() #Options for First paper
    options_list = ""
    for option in options_available_first:   
        
        #TODO: Dealing with none option, Dealing with all nones
        selected_option = Option.objects.get(pk=request.POST[option.opt_name])           
        #except (KeyError, Option.DoesNotExist):
            # Redisplay the application form with error message.
        #    error_message = "You didn't select a choice."
        #    context = get_detail(user, error_message) 
        #    return render_to_response('allotter/apply.html', context, 
        #        context_instance=RequestContext(request))
        #else:
        
        options_list += selected_option.opt_name
        
    user_application.options_selected += options_list   
    user_application.save()
    return HttpResponseRedirect(reverse('allotter.views.complete', args=(reg_no,)))
    #return redirect('/allotter/complete/')
    
#User Application

def complete(request, reg_no):
    
    context = {'user': reg_no}
    ci = RequestContext(request)          
    return render_to_response('allotter/complete.html', context)

"""def quit(request):
	pass
            
"""    

"""def user_register(request):
     Register a new user.
    Create a user and corresponding profile and store roll_number also.

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

"""

