from django import forms
from combo.register.models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['description', 'document','range','name','email']