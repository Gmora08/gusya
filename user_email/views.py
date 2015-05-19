from django.shortcuts import render
from django.views.generic import View

class WaitingListRegistration(View):
    template_name = "registration/index.html"
    def get(self, request):
        return render(request, self.template_name, {})
    def post(self, request):
        return render(request, self.template_name, {})
