from django.shortcuts import render, redirect
from .forms import SighUpForm
from django.contrib.auth.models import User
def create_user(request):
    if request.method !='POST':
        form = SighUpForm()
    else:
        form = SighUpForm(request.POST)
        if form.is_valid():
            user:User = form.save(commit=False)
            user.is_active = True
            user.save()
            send_ver_mail(user, request)
            return redirect('/')
    context = {
        'form':form
    }
    return render(request, 'registration/create_user.html', context)

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import TokenGenerator

account_token_generator = TokenGenerator()

def send_ver_mail(user, request):
    current_site = get_current_site(request)
    mail_subject = 'Your verification link!'
    message = render_to_string('registration/acc_activation_email.html', 
        {
            'user':user,
            'domain':current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_token_generator.make_token(user)
        })
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()

from django.http import HttpResponse
def activate(request, uid, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk = uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("Your account is activated!")
    else:
        return HttpResponse("Activation link is invalid!")