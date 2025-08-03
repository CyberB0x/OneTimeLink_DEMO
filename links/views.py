import os
from datetime import timedelta
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.conf import settings
from .models import OneTimeLink
from .forms import OneTimeLinkForm


def create_link(request):
    """Создание одноразовой ссылки"""
    if request.method == "POST":
        form = OneTimeLinkForm(request.POST, request.FILES)
        if form.is_valid():
            link = form.save()
            # Просто показываем созданную ссылку
            return render(request, 'links/link_created.html', {
                'link': link,
                'access_url': request.build_absolute_uri(f"/access/{link.pk}/")
            })
    else:
        form = OneTimeLinkForm()
    return render(request, 'links/create_link.html', {'form': form})


def access_link(request, pk):
    """Доступ к содержимому ссылки"""
    link = get_object_or_404(OneTimeLink, pk=pk)
    expire_time = link.created_at + timedelta(minutes=link.expiration_minutes)

    # Если срок истёк — удаляем файл и запись
    if timezone.now() > expire_time:
        # Удаляем файл, если существует
        if link.file and os.path.isfile(link.file.path):
            os.remove(link.file.path)
        link.delete()
        return render(request, 'links/link_expired.html')

    # Отображаем файл и текст без удаления
    file_url = link.file.url if link.file else None
    text = link.text

    return render(request, 'links/link_content.html', {
        'file_url': file_url,
        'text': text
    })
