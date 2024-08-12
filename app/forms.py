from django import forms
from app.models import TrainingFile


class QuestionForm(forms.Form):
    question = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


class TrainingFileForm(forms.ModelForm):
    class Meta:
        model = TrainingFile
        fields = ["file"]
