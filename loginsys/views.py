# -*- coding: UTF-8 -*-

from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth

@csrf_exempt
def login(request):
    args = {}

    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "Uncorrect data"
            return render_to_response('login.html')
    else:
        return render_to_response('login.html')

@csrf_exempt
def logout(request):
    print  ')'
    auth.logout(request)
    return redirect('/')