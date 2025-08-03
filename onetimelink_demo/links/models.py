import os
import uuid
from django.db import models


class OneTimeLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_minutes = models.PositiveIntegerField(default=1)
    is_used = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Link {self.pk} ({self.expiration_minutes} min)"
