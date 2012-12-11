from django.db import models
from django.utils.timezone import now
import XenAPI
from contextlib import contextmanager
import urlparse


class ControllableVM(models.Model):
    uri = models.CharField(max_length=256)
    controller = models.ForeignKey('auth.User', related_name="vms")
    last_data_fetch = models.DateTimeField(default=now)
    status = models.CharField(max_length=32, default='Unknown')
    name = models.CharField(max_length=128, default='')

    def log_action(self, message):
        return self.log.create(action=message)

    def get_uuid(self):
        u = urlparse.urlparse(self.uri)
        return u.path[1:]

    @contextmanager
    def get_session(self):
        try:
            url = urlparse.urlparse(self.uri)
            params = { k: v.pop() for k,v in urlparse.parse_qs(url.query).items() }
            session = XenAPI.Session( url.scheme + '://' + url.netloc + '/' )
            session.xenapi.login_with_password ( params['login'], params['password'] )
            yield session
        finally:
            session.close()


    def reload(self, force=False):
        if (now() - self.last_data_fetch).total_seconds() > 10 or force:
            with self.get_session() as session:
                vm = session.xenapi.VM.get_record(session.xenapi.VM.get_by_uuid(self.get_uuid()))
                self.status = vm.get('power_state', 'unknown')
                self.name = vm.get('name_label', 'VM')
                self.last_data_fetch = now()
                self.save()

    def hard_reboot(self):
        with self.get_session() as session:
            task = session.xenapi.Async.VM.hard_reboot( session.xenapi.VM.get_by_uuid(self.get_uuid()))
        self.log.create (action = "Hard reboot by user: " + self.controller.first_name + ' ' + self.controller.last_name)
        self.tasks.create (uuid = task)
        return task

    def pending_tasks(self):
        return self.tasks.filter(active=True)

class ControlActionLog(models.Model):
    vm = models.ForeignKey(ControllableVM, related_name='log')
    when = models.DateTimeField(default=now)
    action = models.TextField()

    class Meta:
        ordering = ['-when']

class ControlTask(models.Model):
    vm = models.ForeignKey(ControllableVM, related_name='tasks')
    uuid = models.TextField(max_length=50)
    active = models.BooleanField(default=True)

    def details(self):
        if self.active:
            with self.vm.get_session() as session:
        	try:
                    task = session.xenapi.task.get_record(self.uuid)
                except XenAPI.Failure:
            	    self.delete()
            	    return inactive
                description = "{name_label} : {status} progress: {progress}".format( **task )
                self.active = task['status'] == 'pending'
                self.save()
                return description
        else:
            return "inactive"