from django.db import models


class LogEntry(models.Model):
    ip = models.GenericIPAddressField()
    date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10)
    uri_request = models.CharField(max_length=50)
    response_code = models.IntegerField()
    bytes = models.IntegerField()

    def __str__(self):
        return self.method
