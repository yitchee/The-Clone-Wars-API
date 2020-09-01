from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View


class DocumentationView(View):
    template_name = 'documentation/documentation.html'

    def get(self, request):
        return render(request, template_name=self.template_name)