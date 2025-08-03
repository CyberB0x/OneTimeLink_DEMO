import os
from datetime import timedelta
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import OneTimeLink
from .forms import OneTimeLinkForm
from django.http import FileResponse

def create_link(request):
    if request.method == "POST":
        form = OneTimeLinkForm(request.POST, request.FILES)
        if form.is_valid():
            link = form.save()
            return render(request, 'links/link_created.html', {'link': link})
    else:
        form = OneTimeLinkForm()
    return render(request, 'links/create_link.html', {'form': form})


def access_link(request, pk):
    link = get_object_or_404(OneTimeLink, pk=pk)

    if link.is_expired():
        # Удаляем файл, если был
        if link.file and os.path.exists(link.file.path):
            os.remove(link.file.path)
        link.delete()
        return render(request, 'links/link_expired.html')

    # Если файл есть — отдаём его как вложение
    if link.file:
        response = FileResponse(open(link.file.path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(link.file.name)}"'
        link.delete()  # удаляем ссылку после скачивания
        return response

    # Если только текст
    text = link.text
    link.delete()
    return render(request, 'links/link_content.html', {'text': text})
