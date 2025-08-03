from django.db import models
from django.utils import timezone
import uuid
import os
from tempfile import gettempdir

def temp_file_path(instance, filename):
    """Хранение во временной папке"""
    return os.path.join(gettempdir(), f"{uuid.uuid4()}_{filename}")

class OneTimeLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=temp_file_path, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    expiration_minutes = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=self.expiration_minutes)

    def __str__(self):
        return f"Link {self.id}"
