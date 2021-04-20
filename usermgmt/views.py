from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from usermgmt.forms import Adduser, Usermod, Userdel, UserGrantAccess, UserForm, UserProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import  pwd
import crypt
import os
import sys
import grp
import smtplib
# Create your views here.

def home(request):
    """ """
    return render(request, 'usermgmt/home.html')

@login_required
def index(request):
    adduser = Adduser()

    context_dict = {'add_user' : adduser}
    return render(request, 'usermgmt/index.html', context_dict)


@login_required
def usershow(request):
    """ """
    return render(request, 'usermgmt/usershow.html', {'userexist': userexist})

@login_required
def addsuccess(request):
    """ """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        expirydate = request.POST.get('expirydate')
        userexist = None
        for user in pwd.getpwall():
            if user[0] == username:
                userexist =  username
                break
        password = password
        encpass = crypt.crypt(password, '22')
        usercheck = os.system("sudo useradd "+username+" -p "+encpass+" -d /data/"+username+" -m -s /bin/bash -e "+expirydate+" -G sftpusers")

        if userexist == username:
           print("User already exist: %s" %username)
        else:
           os.system("sudo mkdir /data/"+username+"/data")
           os.system("sudo chown root:root /data/"+username)
           os.system("sudo chown -R "+username+":"+username+" /data/"+username+"/data")
           os.system("sudo chmod 755 /data/"+username)
           print("User Doesn't exist in the server")
           print("Creating the User: %s" %username)
           print("Sending initial email to "+email)
           sender = 'admin@ftp.globalconnect.dk'
           receivers = [ email ]

           message = """From: SFTP Admin <admin@ftp.globalconnect.dk>
           To: To Person <"""+email+""">
           Subject: SMTP e-mail test
           
           Dear Customer

           Your account are ready for use. To access our secure ftp service, you can use WinSCP.

           Address: ftp.globalconnect.dk
           Your username is: """+username+"""

           Your password will be delivered from our technician.

           GlobalConnect

           Service Desk 
           """
           try:
              smtpObj = smtplib.SMTP('localhost',25)
              smtpObj.sendmail(sender, receivers, message)
              smtpObj.quit()
              print("Successfully sent email")
           except smtplib.SMTPException:
              print("Error: unable to send email")
           

    return render(request, 'usermgmt/addsuccess.html', {'userexist': userexist, 'username': username})

@login_required
def usermod(request):
    """ """
    adduser = Usermod()

    context_dict = {'user_mod' : adduser}
    return render(request, 'usermgmt/usermod.html', context_dict)

@login_required
def modifyuser(request):
    """ """
    if request.method == 'POST':
        username = request.POST.get('username')
        new_expirydate = request.POST.get('new_expirydate')
        os.system("sudo chage -E "+new_expirydate+" "+username)

    return render(request, 'usermgmt/usermodsucc.html', {'username': username, 'new_expirydate': new_expirydate})


@login_required
def userdel(request):
    """ """
    userdel = Userdel()

    context_dict = {'user_del' : userdel}
    return render(request, 'usermgmt/userdel.html', context_dict)


@login_required
def deleteduser(request):
    """ """
    if request.method == 'POST':
        username = request.POST.get('username')
        for user in pwd.getpwall():
            if user[0] == username:
                username = username
                break
        user_logged = os.system("who | cut -d' ' -f1 | sort | uniq > user.txt")
        fr = open('user.txt', 'r')
        for userlog in fr:
            if userlog == username:
                return userlog
        fr.close()
        user_delete = os.system("sudo userdel -r "+username+"")
        group_delete = os.system("sudo groupdel "+username+"")
        data_delete = os.system("sudo rm -rf /data/"+username)
        if user[0] == username:
            username = username
        else:
            username = None

    return render(request, 'usermgmt/userdelsucc.html', {'username': username, 'userlog': userlog})

@login_required
def usergrant(request):
    """ """
    usergrant = UserGrantAccess()

    context_dict = {'user_grant' : usergrant}
    return render(request, 'usermgmt/usergrant.html', context_dict)

@login_required
def grantusersucc(request):
    """ """
    if request.method == 'POST':
        username = request.POST.get('username')
        for user in pwd.getpwall():
            if user[0] == username:
                username = username
                break

        if user[0] == username:
            username = username
            get_sudoers_file = os.system("sudo cp /etc/sudoers .")
            get_sudo_tmp = os.system("sudo cp sudoers sudoers.tmp")
            change_permission = os.system("sudo chmod 777 sudoers")
            grant_sudo_access = '%s ALL=(ALL) ALL' %username
            print(grant_sudo_access)
            with open('sudoers', 'a') as fr:
                fr.write('\n')
                fr.write(grant_sudo_access)
            read_only_permission = os.system("sudo chmod 044 sudoers")
            get_sudo_access = os.system("sudo cp sudoers /etc/sudoers")
        else:
            username = None

    return render(request, 'usermgmt/usergrantsucc.html', {'username': username})

@login_required
#@user_passes_test(lambda u: u.is_superuser)
def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user


            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'usermgmt/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )




def user_login(request):
   #If the request is HTTP POST, try to pull out the relevent information
   if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')
      user = authenticate(username=username, password=password)
      if user:
          #Is the account active? It could have disabled
          if user.is_active:
              # If the account is valid and active, we can login the user in
              # We'll send the user bact to the homepage
              login(request, user)
              return HttpResponseRedirect('/home')
          else:
              # An active account was used - no logging in
              return HttpResponse("Your account got disabled")
      else:
          # Bad login details were provided, So we can't log the user in
          print("Invalid login details: {0}, {1}".format(username, password))
          return HttpResponse("Invalid login details supplied.")
   # This scenario would most likely be a HTTP GET.
   else:
      # No context variables to pass to the template system, hence the
      # blank dictionay object...
      return render(request, 'usermgmt/login.html')

def user_logout(request):
    logout(request)

    #Take the user back to the homepage
    return HttpResponseRedirect('/')

