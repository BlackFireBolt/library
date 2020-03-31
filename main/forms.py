from django import forms
from django.forms import inlineformset_factory
from storages.backends.sftpstorage import SFTPStorage
from django.http import HttpResponse, Http404
import mimetypes

from .models import SuperCategory, SubCategory
from .models import Article

sfs = SFTPStorage()


class SubCategoryForm(forms.ModelForm):
    super_category = forms.ModelChoiceField(queryset=SuperCategory.objects.all(), empty_label=None, label='Кафедра', required=True)
    
    class Meta:
        model = SubCategory
        fields = '__all__'


class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=20, label='')

