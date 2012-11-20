from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

@login_required(login_url="/accounts/login/")
def big_red_restart_button(request):
    return TemplateResponse(request, "restart_button.html", { 'user' : auth.get_user(request)} )

@login_required(login_url="/accounts/login/")
def do_restart(request, vm_id):
    return HttpResponseRedirect("/restart")