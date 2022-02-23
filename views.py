from django.shortcuts import render, redirect, get_object_or_404
from myapp.forms import FileUploadForm
from django.contrib import messages
from myapp.models import File
import os
from myapp.graphpy import graphpy
from django.http import FileResponse


def index(request):
    all_data = File.objects.all()
    context = {
        'title': 'グラフ作成アプリケーション',
        'all_data': all_data,
    }
    return render(request, 'index.html', context)


def upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'アップロードに成功しました')
            return redirect('index')
    else:
        form = FileUploadForm()
    context = {
        'title': 'ファイルのアップロード',
        'form': form,
    }
    return render(request, 'upload.html', context)
    
    
def delete(request, id):
    delete_data = get_object_or_404(File, pk=id)
    delete_file = delete_data.file.url
    os.remove(delete_file[1:])
    delete_data.delete()
    messages.success(request, 'データを削除しました')
    return redirect('index')


def graph(request, id):
    data = get_object_or_404(File, pk=id)
    file_path = data.file.url[1:]
    graphpy(file_path)
    messages.success(request, 'グラフが作成できました')
    return redirect('index')


def dd(request):
    files = os.listdir('download')
    context = {
        'title': 'ダウンロード・削除',
        'files': files,
    }
    return render(request, 'dd.html', context)


def download(request, path):
    download_path = 'download/' + path
    return FileResponse(open(download_path, "rb"), as_attachment=True)


def output_delete(request, path):
    delete_file_path = 'download/' + path
    os.remove(delete_file_path)
    return redirect('dd')

