from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Company
from django.urls import reverse
from .helper import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
#from django.utils.decorators import method_decorator
#from .decorators import *
#from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib import messages

# Create your views here.

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/upload_cloud/')
        else:
            messages.error(request, '존재하지 않는 사용자입니다.')
            return render(request, 'login.html')
    return render(request, 'login.html')

def join(request):
    if request.session['agreement'] == False:
        messages.error(request, '잘못된 접근입니다. 정상적인 경로로 접근하세요.')
        return render(request, 'main.html')

    if request.method=='POST':
        if request.POST['password']==request.POST['password_check']:
            username=request.POST['username']

            if User.objects.filter(username=username).exists():
                messages.error(request, '이미 사용 중인 Email입니다!')
                return render(request, 'join.html')

            user=User.objects.create_user(
                username=username,
                password=request.POST['password'],
            )
            user.is_active=False
            user.save()
            company=Company()
            company.user=user
            company.com_name=request.POST['com_name']
            company.com_major=request.POST['com_major']
            company.save()

            send_mail(
                '{}님의 회원가입 인증메일 입니다.'.format(user.username),
                [user.username],
                html=render_to_string('join_email.html', {
                    'user': user,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                    'domain': request.META['HTTP_HOST'],
                    'token': default_token_generator.make_token(user),
                }),
            )
            return redirect(get_success_url(request))
        else:
            messages.error(request, '비밀번호가 다릅니다!')
            return render(request, 'join.html')
    else:
        return render(request, 'join.html')

def activate(request, uid64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid64))
        current_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        messages.error(request, '메일 인증에 실패했습니다.')
        return redirect('/')

    if default_token_generator.check_token(current_user, token):
        current_user.is_active = True
        current_user.save()

        messages.info(request, '메일 인증이 완료 되었습니다. 회원가입을 축하드립니다!')
        return redirect('/register/login/')

    messages.error(request, '메일 인증에 실패했습니다.')
    return redirect('/register/main/')

def get_success_url(request):
    request.session['agreement'] = False
    request.session['register_auth'] = True
    messages.success(request, '입력한 Email 주소로 인증 메일이 발송되었습니다. 인증 후 로그인이 가능합니다.')
    return reverse('join_success')

def join_success(request):
    if not request.session.get('register_auth', False):
        raise PermissionDenied
    request.session['register_auth'] = False

    return render(request, 'join_success.html')

def logout(request):
        auth.logout(request)
        return redirect('/')

def agreement(request):
    if request.method=='POST':
        if request.POST.get('agreement1', False) and request.POST.get('agreement2', False):
            request.session['agreement'] = True
            return redirect('/register/join/')
        else:
            messages.info(request, "약관에 모두 동의해주세요.")
            return render(request, 'agreement.html')
    else:
        request.session['agreement'] = False
        return render(request, 'agreement.html')