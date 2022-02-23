from django.forms import ModelForm
from myapp.models import File


class FileUploadForm(ModelForm):
    class Meta:
        model = File
        fields = ('name', 'title', 'file')
        