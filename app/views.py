from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.views.decorators.csrf import csrf_protect

import random
from .forms import EmployeeForm
from django.http import HttpResponse
from .models import EmployeeRegistration, Timestamp
from random import randint
import string
import datetime
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import User
from django.contrib import messages
from django.core.mail import EmailMessage
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.start()
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError


# Signup
def signupform(request):
    return render(request, 'employee.html', {'form': EmployeeForm})


# Signup form for employee
def Signup(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST or None)
        if form.is_valid():
            if EmployeeRegistration.objects.filter(email=form.cleaned_data['email']).exists():
                msg = " your email is already exists"
                return render(request, 'employee.html', {'form': EmployeeForm, 'msg': msg})
            else:
                employee = EmployeeRegistration()
                employee.name = form.cleaned_data['name']
                employee.contact_no = form.cleaned_data['contact_no']
                employee.email = form.cleaned_data['email']
                employee.designation = form.cleaned_data['designation']
                employee.department = form.cleaned_data['department']
                employee.jobs = form.cleaned_data['jobs']
                employee.date_of_joining = form.cleaned_data['date_of_joining']
                d = str(employee.date_of_joining).split("-")
                generate = {
                    'Intern': 9,
                    'Full_time': 1
                }
                e_id = str(generate[employee.designation]) + str(randint(100, 999)) + str(d[1] + str(d[0]))

                employee.Employeeid = e_id
                password = generate_random_password()
                employee.password = password
                user = User.objects.create_user(e_id, password=password)
                employee.user = user
                employee.save()
                user.email=form.cleaned_data['email']
                user.save()
                body = 'Welcome in Lampros.Tech !!<br> Your Employee Id is :-  ' + e_id + "<br> Your Password is :- " + password
                if send_mail_custom(form.cleaned_data['email'], body):
                    msg = 'You are Successfully Signup.Please Check your Email for Login.'
                    fm = AuthenticationForm()

                    return render(request, 'login.html', {'msg': msg, 'form': fm})
                else:
                    msg = "you have't signup Properly."

                return render(request, 'login.html', {'msg': msg})
    else:
        form = EmployeeForm()

    return render(request, 'employee.html', {'form': EmployeeForm})


alphabets = list(string.ascii_letters)
digits = list(string.digits)
special_characters = list("!@#$%^&*()")
characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")


def generate_random_password():
    ## length of password from the user
    length = 6

    ## number of character types
    alphabets_count = 2
    digits_count = 2
    special_characters_count = 2

    characters_count = alphabets_count + digits_count + special_characters_count

    ## initializing the password
    password = []

    ## picking random alphabets
    for i in range(alphabets_count):
        password.append(random.choice(alphabets))

    ## picking random digits
    for i in range(digits_count):
        password.append(random.choice(digits))

    ## picking random alphabets
    for i in range(special_characters_count):
        password.append(random.choice(special_characters))

    ## if the total characters count is less than the password length
    ## add random characters to make it equal to the length
    if characters_count < length:
        random.shuffle(characters)
        for i in range(length - characters_count):
            password.append(random.choice(characters))

    ## shuffling the resultant password
    random.shuffle(password)

    ## converting the list to string
    ## printing the list
    return "".join(password)


# LOGIN Employee
def User_login(request):
    if request.method == "POST":
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                if user.username == "7891234":

                    login(request, user)

                    return HttpResponseRedirect('/emp_detail/')
                else:
                    login(request, user)
                    if not scheduler.get_job(user.username):
                        exists = Timestamp.objects.filter(Employeeid=request.user.username,
                                                          login_time__startswith=datetime.date.today())
                        if exists:
                            pass
                        else:
                            employee = EmployeeRegistration.objects.get(Employeeid=user.username)
                            time = Timestamp()
                            time.name = employee.name
                            time.Employeeid = employee
                            time.save()

                        dd = datetime.datetime.now() + datetime.timedelta(hours=12)
                        scheduler.add_job(logout_update, 'date', run_date=dd, kwargs={'user': user, 'request': request},
                                          id=user.username)

                    return HttpResponseRedirect('/profile/')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        fm = AuthenticationForm()
    return render(request, 'login.html', {'form': fm})


# Employee Profil
def user_profile(request):
    emp_id = request.user.username
    emp_data = EmployeeRegistration.objects.get(Employeeid=emp_id)
    t_stamp = Timestamp.objects.filter(Employeeid=emp_id).last()
    total_time = Timestamp.objects.all()
    return render(request, 'profile.html',
                  {'name': request.user, 'emp_data': emp_data, 't_stamp': t_stamp, 'total_time': total_time})


@login_required
# Logout
def logout_view(request):
    if request.user.username == "7891234":
        logout(request)

    else:
        now = datetime.datetime.now()
        time = Timestamp.objects.filter(Employeeid=request.user.username).last()
        time.logout_time = now
        time.save()
        scheduler.remove_job(request.user.username)
        logout(request)
    return redirect('login')


def logout_update(user, request):
    now = datetime.datetime.now()
    print("in")
    time = Timestamp.objects.filter(Employeeid=user.username).last()
    time.logout_time = now
    time.save()
    logout(request)
    scheduler.remove_job(user.username)



@login_required
# Employee_detail for office Purpose
def employee_detail(request):
    queryset = EmployeeRegistration.objects.all()
    return render(request, 'emp_detail.html', {'detail': queryset})


def detail(request):
    id = request.GET.get('emp_id')
    e_data = EmployeeRegistration.objects.get(Employeeid=id)
    queryset = Timestamp.objects.filter(Employeeid=id)
    return render(request, 'detail.html', {'e_data': e_data, 'queryset': queryset})


# Change Password
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        if request.user.check_password(current_password):
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if (len(new_password.strip()) > 5 and len(new_password.strip()) < 11):
                if new_password == (confirm_password):
                    request.user.set_password(new_password)
                    request.user.save()
                    fm = AuthenticationForm()
                    try:
                        scheduler.remove_job(request.user.username)
                    except:
                        print('error')
                    logout(request)
                    return redirect('login')
                else:
                    msg = "New password and confirm password are not match"
                    return render(request, 'changepassword.html', {'msg': msg})
            else:
                msg = "Password must be 6 to 10 Character"
                return render(request, 'changepassword.html', {'msg': msg})
        else:
            msg = "Old Password is invalid"
            return render(request, 'changepassword.html', {'msg': msg})
    else:
        return render(request, 'changepassword.html')




# Password Reset Done
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        print(user.email)
                        send_mail(subject, email, 'testlampros@gmail.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    else:
        password_reset_form = PasswordResetForm()
        return render(request=request, template_name="password_reset.html",
                      context={"password_reset_form": password_reset_form})


# Email for employeeid and Password
def send_mail_custom(email, body):
    to = email
    subject = 'Your Lampros.Tech Login Credentials'
    body = body
    email = EmailMessage(subject, body, to=(to,))
    email.content_subtype = "html"
    if (email.send()):
        return True
    else:
        return False
