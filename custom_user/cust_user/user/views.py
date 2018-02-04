from .email_send_file import send_email
from .send_sms import sendSMS
from .generate_token import generate_code
from django.utils.encoding import smart_text
import time
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UserLoginForm, UserRegisterForm

User = get_user_model()


# home page view
def home_view(request):
    return render(request, 'home.html', {})


# login view
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    title = "Login"
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        end = round(time.time())
        start = request.session.get('start_time', None)
        if start is None:
            return render(request, "login.html", {"form": form, "title": title, 'error':'There was a Problem Send Otp Again'})

        time_spent = end-start

        if time_spent < 30:
            email = form.cleaned_data.get("email")
            token = form.cleaned_data.get('token')
            session_token = request.session.get('token', 'token_not_recevied')

            if session_token == 'token_not_recevied':
                return render(request, "login.html", {"form": form, "title": title, 'error': 'Please Get OTP..Try Again'})

            if session_token == token:
                user = authenticate(request, email=email)
                print(user)
                login(request, user)
                if next:
                    return redirect(next)
                return redirect("/")

    return render(request, "login.html", {"form":form, "title": title})


# register view
def register_view(request):
    next = request.GET.get('next')
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Registered')
        if next:
            return redirect(next)
        return redirect("login")

    context = {
        "form": form,
        "title": title
    }
    return render(request, "signup.html", context)


# logout view
def logout_view(request):
    logout(request)
    return redirect("/")


# ajax generate token
def generate_token(request):
    if request.is_ajax():   # if  ajax request
        number_or_email = request.GET.get('number_or_email')
        number_or_email = smart_text(number_or_email, encoding='utf-8')   # decode the data
        if number_or_email == '':
            data = {
                'message': "number/email cannot be blank"
            }
            return JsonResponse(data)

        number_user_qs = User.objects.filter(phone_number=number_or_email)
        email_user_qs = User.objects.filter(email=number_or_email)

        number_exist = number_user_qs.exists()
        email_exist = email_user_qs.exists()

        if number_exist or email_exist:
            token = str(generate_code()) # generate token
            if number_exist:            # number_exist ...
                number_user = number_user_qs.first().phone_number   # get object number
                try:
                    resp = sendSMS(number=number_user, message=token)  # send otp through sms
                except:
                    data = {
                        'message': "Internet Error"
                    }
                    return JsonResponse(data)
                if resp == -1:
                    message = "There was a problem with sms gateway"
                if resp['status'] == 'success':
                    request.session['start_time'] = round(time.time())
                    request.session['token'] = token
                    message = "Sms Sent"
                if resp['status'] == 'error':
                    message = "Error in sending otp..try again"
                if resp['status'] == 'failure':
                    message = "Error with sms gateway"
            else:
                email_user = email_user_qs.first().email  # email exist get object email
                try:
                    email_status = send_email(email_user=email_user, token=token)   # send otp through email
                except:
                    data = {
                        'message': "Internet Error"
                    }
                    return JsonResponse(data)

                # check if email sent successfully
                if email_status == -1:
                    message = "Error with either otp or email... Try Again"
                if email_status == 1:
                    request.session['start_time'] = round(time.time())
                    request.session['token'] = token
                    message = "OTP sent successfully"
                if email_status == 0:
                    message = "Failure in sending email.Try Again"
        else:
            message = "There is no such number/email"
    data = {
        'message': message
    }
    return JsonResponse(data)


