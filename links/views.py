import os
from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from .models import OneTimeLink
from .forms import OneTimeLinkForm


def create_link(request):
    if request.method == "POST":
        form = OneTimeLinkForm(request.POST, request.FILES)
        if form.is_valid():
            link = form.save()
            return render(request, 'links/link_created.html', {'link': link})
        else:
            # Отладка: выводим ошибки формы в лог
            print(form.errors)
    else:
        form = OneTimeLinkForm()
    return render(request, 'links/create_link.html', {'form': form})


def access_link(request, pk):
    link = get_object_or_404(OneTimeLink, pk=pk)

    if link.is_expired():
        if link.file and os.path.exists(link.file.path):
            os.remove(link.file.path)
        link.delete()
        return render(request, 'links/link_expired.html')

    if link.file:
        file_path = link.file.path
        filename = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            response = FileResponse(f, as_attachment=True, filename=filename)
        link.delete()
        return response

    text = link.text
    link.delete()
    return render(request, 'links/link_content.html', {'text': text})
