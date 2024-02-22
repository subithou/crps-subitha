from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect

from home.models import AuthenticationBackend


# Create your views here.

def home_page(request):
    return render(request, 'homePage.html')


def login_page(request):
    if request.method == 'POST':
        username1 = request.POST.get('username')
        password1 = request.POST.get('password')

        if AuthenticationBackend.authenticate(self=None, request=request, username=username1,
                                              password=password1) is not None:
            user = AuthenticationBackend.authenticate(self=None, request=request, username=username1,
                                                      password=password1)

            login(request, user)
            # Redirect to a success page.
            return redirect('customer_home')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'loginPage.html')

    return render(request, 'loginPage.html')
