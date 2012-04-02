from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render, redirect, get_object_or_404

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect 

from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from allotter.models import Profile, Option, Exam
from allotter.forms import UserLoginForm, UserDetailsForm

from itertools import chain
from django.core.mail import send_mail, mail_admins

#Reportlab libraries
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY

import time

def user_login(request):
    """
        Verify the user credentials and log the user in.
    """

    user = request.user
    if user.is_authenticated():
        status = user.get_profile().application.submitted #Getting the submission status
        if status: #If already submitted, takes to Completion Page
            return redirect('/allotter/complete/')
        else: #Otherwise to Details Submission form 
            return redirect('/allotter/details/')

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            login(request, user)
            status = user.get_profile().application.submitted #Getting the submission status          
            if status:
                return redirect('/allotter/complete/') #Redirect to Completion Page
            else:  
                return redirect('/allotter/details/')  #Redirect to user details submission 
        else:
            context = {"form": form}
            return render(request, 'allotter/login.html', context)
    else:
        form = UserLoginForm()
        context = {"form": form}
        return render(request, 'allotter/login.html', context)
                                     

@login_required
def submit_details(request):
    """
        Get the secondary email address, phone number and save it to the Profile.
    """
    user = request.user
    category = user.get_profile().application.cgy #Getting the Category information
    #Flag set based on OBC Check
    if category == "B": cat_flag = True
    else: cat_flag = False  
    if request.method == "POST":
        form = UserDetailsForm(user, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            form.save()
            return redirect('/allotter/apply/') #Details submitted, taken to application page
        else:
            return render(request, 'allotter/details.html', {'form':form})  
                
    else:
        form = UserDetailsForm(request.user)
        context = {"form": form, "cat_flag": cat_flag}
        return render(request, 'allotter/details.html', context)              
       
def get_details(user, error_message = ""):
    """
       Retrieves the information about Test paper(s) and options available
       and returns them in a dictionary(context) for passing to the Template.
    """
    user_profile = user.get_profile()
    user_application = user_profile.application
    np = user_application.np #Number of Papers
    first_paper = user_application.first_paper #First Paper Name
    first_paper_code = first_paper.exam_code
    options_available_first = Option.objects.filter(exam__exam_name=first_paper).distinct() #Options for First paper
    oafl = len(options_available_first)  
    if np == 2: #If written two exams
        second_paper = user_application.second_paper
        second_paper_code = second_paper.exam_code
        options_available_second = Option.objects.filter(exam__exam_name=second_paper).distinct()
        oasl = len(options_available_second)
        context = {'user': user, 'first_paper': first_paper,
            'options_available_first' : options_available_first,
            'first_paper_code' : first_paper_code, 
            'second_paper': second_paper, 'second_paper_code': second_paper_code,
            'options_available_second' : options_available_second,
            'np' : np, 'options_range': range(1, oafl + oasl + 1, 1), 
            'error_message': error_message}    
    else: #If written only one exam
        context = {'user': user, 'first_paper': first_paper,
            'first_paper_code' : first_paper_code,
            'options_available_first' : options_available_first,
            'options_range': range(1, oafl + 1, 1), 
            'np' : np, 'error_message' : error_message}     
    return context              
                                     
@login_required
def apply(request):
    """
        Displays the application page for an authenticated user.
    """
    user = request.user
    if not(user.is_authenticated()):
        return redirect('/allotter/login/')
    
    context = get_details(user) 
              
    return render(request, 'allotter/apply.html', context)                         


def user_logout(request):
    ##Logouts the user.
    logout(request)
    return redirect ('/allotter/login/')
    
##http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-##order    
def rem_dup(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]
    

#TODO: Extensive Testing
@login_required                            
def submit_options(request):
    """
        Gets the Options and their preference number through the POST object and
        stores them as list(sorted according to preferences). Options with None are 
        ignored. 
    """
    reg_no = request.user.username
    user = get_object_or_404(User, username=reg_no)
    user_profile = user.get_profile()
    user_application = user_profile.application
    np = user_application.np
    first_paper = user_application.first_paper #First Paper Name
    options_available_first = Option.objects.filter(exam__exam_name=first_paper).distinct() #Options for First paper
    
    if np == 2: #If qualified for second paper
        second_paper = user_application.second_paper #Second Paper Name
        options_available_second = Option.objects.filter(exam__exam_name=second_paper).distinct() #Options for second paper
        options_available_list = chain(options_available_first, options_available_second) #chaining the two lists
    else:
        options_available_list = options_available_first
        
    options_chosen_list = [] #Initializing empty list for storing options
 
    for option in options_available_list:   
        option_pref = request.POST[unicode(option.opt_code)]           
        options_chosen_list.append([int(option_pref), str(option.opt_code)]) #[preference, option code]
    
      
    options_chosen_list.sort() #Sorting by preference
    options_code_list = []
    for opt in options_chosen_list:
        if int(opt[0]): #ignoring the options for which None was marked
            options_code_list.append(opt[1])
        
    user_application.options_selected = options_code_list #Saving the data in model   
    user_application.submitted = True #Submission Status
    user_application.save() 
    return redirect('/allotter/complete/')


def complete_allotment(request):
    """
        Passes the chosen options queryset to the Completion Page Template
    """
    reg_no = request.user.username
    user = get_object_or_404(User, username=reg_no)
    sec_email = user.get_profile().secondary_email
    options_chosen = get_chosen_options(user)
    context = {'username': reg_no, 'email': sec_email,  
                'options_chosen': options_chosen}
    ##Sending mail with allotment details             
    admin = User.objects.get(pk=1)            
    from_email = admin.email
    subject = "JAM 2012 admissions"
    content = "The following options were chosen by you \n \n"
    if options_chosen:
        counter = 1
        for option in options_chosen:
            content += "Preference Number: %s, Option Code: %s, Option Name: %s, Location: %s \n"  %(counter, option.opt_code, option.opt_name, option.opt_location)
            counter += 1 
                            
    content += "\n \n \nPlease do not delete this email and keep it for reference purposes. \n \n \n \n Regards, \n JAM Office, IIT Bombay"
    send_mail(subject, content, from_email, [sec_email])
    admin_content = content
    admin_content +="\n\n\n#%s:" % (reg_no)
    counter = 1
    for option in options_chosen:
            admin_content += "%s,%s:"  %(counter, option.opt_code) 
            counter += 1
    admin_content +="#"
    admin_content += time.ctime()                      
    mail_admins(subject, admin_content)                   
    return render(request, 'allotter/complete.html', context)
    
    
def get_chosen_options(user):
    """
        Reads the options submitted by the user in the Application page
    """
    user_profile = user.get_profile()
    user_application = user_profile.application
    np = user_application.np
    ocl = eval(user_application.options_selected)
    chosen_options = []
    for oc in ocl:
        chosen_options.append(Option.objects.get(opt_code=int(oc))) 
    return chosen_options
        
        
@login_required        
def generate_pdf(request):
    """
        The Ugly code for generating the pdf using ReportLab.
    """
    reg_no = request.user.username
    user = get_object_or_404(User, username=reg_no)
    user_profile = user.get_profile()
    user_application = user_profile.application
    np = user_application.np
 
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=JAM2012_Allottment.pdf'
    
    elements = []
    doc = SimpleDocTemplate(response)
    
    formatted_time = time.ctime()
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    
    ptext = '<font size=15>JAM 2012 - Admissions.</font>'         
    elements.append(Paragraph(ptext, styles["Justify"]))
    elements.append(Spacer(4, 20))
    
    ptext = '<font size=12>Registration Number: %s</font>' % reg_no 
    elements.append(Paragraph(ptext, styles["Normal"]))
    elements.append(Spacer(1, 12))
     
    data = []   
    options = get_chosen_options(user) ##Put a check to show when the options chosen is empty
    
    if not(options):
        ptext = '<font size=12>No choices were selected.</font>' 
        elements.append(Paragraph(ptext, styles["Normal"]))
        elements.append(Spacer(1, 12))
        doc.build(elements) 
        return response 
        
    ptext = '<font size=12>The choices selected by me are as follows: </font>' 
    elements.append(Paragraph(ptext, styles["Normal"]))
    elements.append(Spacer(4, 30))
        
    counter = 1
    for opt in options:
        data.append([counter, opt.opt_code, opt.opt_location, opt.opt_name])
        counter = counter + 1
            
    t = Table(data)
    t.setStyle(TableStyle([('GRID',(0,0),(3,len(options)),1,colors.black),
                                   ('TEXTCOLOR',(0,0),(0,-1),colors.green)]))
                                                                     
    elements.append(t)  
    
    elements.append(Spacer(4, 30))
          
    ptext = '<font size=12>I hereby declare that the order of preference given by me for my eligible programmes is final. </font>' 
    elements.append(Paragraph(ptext, styles["Normal"]))
    elements.append(Spacer(4, 25))
    
    ptext = '<font size=12>Signature of the Candidate</font>' 
    elements.append(Paragraph(ptext, styles["Normal"]))
    elements.append(Spacer(4, 20))
        
    ptext = '<font size=12>%s</font>' % formatted_time
    elements.append(Paragraph(ptext, styles["Normal"]))
    elements.append(Spacer(1, 12))
 
    doc.build(elements)
       
    return response    
    


