from django.db import models


class ControllableVM(models.Model):
    uri = models.CharField(max_length=256)
    controller = models.ForeignKey('auth.User', related_name="vms")

    def get_uuid(self):
        import urlparse
        u = urlparse.urlparse(self.uri)
        return u.path[1:]


