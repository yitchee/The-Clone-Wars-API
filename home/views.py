from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import TemplateView, View

from rest_framework.response import Response

from users.models import User
from .forms import SignUpForm

import time
def index(request):
    return render(request, 'home/index.html')


class SignUpView(View):
    template_name = 'home/signup.html'

    def get(self, request):
        # print(request.META['HTTP_ORIGIN'], request.build_absolute_uri('/'))
        context = {}
        context['signup_form'] = SignUpForm()
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data.get('email')
            if not User.objects.filter(email=new_email):
                new_user = User()
                new_user.email = new_email
                User.objects.create_user(new_email)
                response = JsonResponse({"success": "API Key success"})
            else:
                response = JsonResponse({"error": "API Key success"}, status=400)

        return response