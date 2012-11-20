from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
import models
import XenAPI

@login_required(login_url="/accounts/login/")
def big_red_restart_button(request):
    user = auth.get_user(request)
    map(lambda vm: vm.reload(), user.vms.all())
    return TemplateResponse(request, "restart_button.html", { 'user' : user} )

@login_required(login_url="/accounts/login/")
def do_restart(request, vm_id):
    try:
        cvm = models.ControllableVM.objects.get(pk=vm_id)
        assert cvm.controller == request.user, "Unauthorized"
        task = cvm.hard_reboot()
        cvm.reload(True)
    except XenAPI.Failure, e:
        messages.error(request, `e` + ' ' + `e.details`)
    except Exception, e:
        messages.error(request, `e` + ' ' + `e.message`)
    return HttpResponseRedirect(reverse("restart:index"))