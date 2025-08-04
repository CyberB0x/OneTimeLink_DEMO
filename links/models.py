from django.db import models
from django.utils import timezone
import uuid
import os

def temp_file_path(instance, filename):
    """Сохраняем файлы во временную папку внутри MEDIA_ROOT/tmp"""
    return os.path.join('tmp', f"{uuid.uuid4()}_{filename}")

class OneTimeLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=temp_file_path, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    expiration_minutes = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=self.expiration_minutes)

    def delete_file(self):
        """Удаляет файл, если он есть"""
        if self.file and self.file.storage.exists(self.file.name):
            self.file.delete(save=False)

    def __str__(self):
        return f"Link {self.id}"
