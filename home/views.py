from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import TemplateView, View

from rest_framework.response import Response

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
        time.sleep(.5)
        form = SignUpForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data.get('email'))
        response = JsonResponse({"success": "API Key success"})
        return response