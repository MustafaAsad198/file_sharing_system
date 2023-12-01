
# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, File
from .forms import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')

def ops_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['passwrd']
        try:
            user=User.objects.get(username=username,passwrd=password)
            if user.user_type=='CL':
                return HttpResponse("This user is registered as a Client user. Use 'Login as Client User' to get access.")
            user.is_active=True
            user.save()
            if user.is_active:
                return redirect(f'/ops-upload/{user.username}')
        except Exception as e:
            return HttpResponse('Invalid credentials')
    else:
        return render(request, 'ops_login.html')

@login_required(login_url='/ops_login/')
def ops_upload(request,pk):
    user=User.objects.get(username=pk)
    if request.method == 'POST':

        file = request.FILES['file']
        complete_file_name=file.name
        file_type = complete_file_name.split('.')[-1]
        file_name=complete_file_name.split('.')[0]
        if file_type not in ('pptx', 'docx', 'xlsx'):
            return HttpResponse('Invalid file type')

        file = File.objects.create(file_name=file_name, file_type=file_type, uploaded_by=user,file=file)
        file.save()
        return redirect(f'/ops-upload/{user.username}')
    else:
        return render(request, 'ops_upload.html',context={'user':user})

def client_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        print(form)
        username = form['username'].value()
        if User.objects.filter(username=username).exists():
            return HttpResponse(f'Username "{username}" is already in use.')
        email = form['email'].value()
        if User.objects.filter(email=email).exists():
            return HttpResponse(f'Email address "{email}" is already in use.')
        if form.is_valid():
            user=User(username=form['username'].value(),email=form['email'].value(),passwrd=form['passwrd'].value(),user_type='CL')
            user.save()
            # Send verification email
            verification_link = f'http://127.0.0.1:8000/verify-email/{user.pk}'
            email_content = f'Please click the following link to verify your email: {verification_link}'
            recepient=[user.email, ]
            sender=settings.EMAIL_HOST_USER
            subject='Recent Registration Activity has been witnessed with this account'
            # Send email using your preferred email sending method
            print(sender,recepient)
            send_mail(subject,email_content,sender,recepient)

            return HttpResponse(f'Please verify your email to complete your registration. Login to continue. An email is sent to you at {user.email}')
        else:
            return redirect('home')
    else:
        form = SignupForm()
        return render(request, 'client_signup.html', {'form': form})

def client_verify_email(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse('Invalid verification link')

    if user.is_active:
        return HttpResponse('Your email has already been verified')

    user.is_active = True
    user.save()

    return redirect('client_login')


def client_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['passwrd']
        try:
            user=User.objects.get(username=username,passwrd=password)
            if user.user_type=='OP':
                return HttpResponse("This user is registered as a Operation user. Use 'Login as Operation User' to get access.")
            user.is_active=True
            user.save()
            if user.is_active:
                return redirect(f'/client-home/{user.username}')
        except Exception as e:
            return HttpResponse('Invalid credentials')
    else:
        return render(request, 'client_login.html')

def ops_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        username = form['username'].value()
        if User.objects.filter(username=username).exists():
            return HttpResponse(f'Username "{username}" is already in use.')
        email = form['email'].value()
        if User.objects.filter(email=email).exists():
            return HttpResponse(f'Email address "{email}" is already in use.')
        if form.is_valid():
            user=User(username=form['username'].value(),email=form['email'].value(),passwrd=form['passwrd'].value(),user_type='OP')
            user.save()
            return redirect('/ops-login/')
        else:
            return render(request, 'ops_signup.html', {'form': form})
    else:
        form = SignupForm()
        return render(request, 'ops_signup.html', {'form': form})


@login_required(login_url='/client-login/')
def client_home(request,pk):
    user=User.objects.get(username=pk)
    files=File.objects.all()
    return render(request, 'client_home.html',context={'user':user, 'files':files})

@login_required(login_url='/ops-login/')
def ops_logout(request,pk):
    user=User.objects.get(username=pk)
    if user.is_active!=True:
        return JsonResponse(f'{user.username} not logged in.',safe=False)
    user.is_active=False
    user.save()
    return redirect('home')

@login_required(login_url='/client-login/')
def client_logout(request,pk):
    user=User.objects.get(username=pk)
    if user.is_active!=True:
        return JsonResponse(f'{user.username} not logged in.',safe=False)
    user.is_active=False
    user.save()
    return redirect('home')

@login_required(login_url='/client-login/')
def download_files(request,pk):
    if request.method=='POST':
        file=File.objects.get(id=pk)
    return render(request,'download_file.html',context={'download_link':f'http://127.0.0.1:8000/download-file/{file.id}','message':'success','file':file})