from django import forms

class AddFrom(forms.Form):
    content = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'placeholder':'Название'}))
    deadline = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'], widget=forms.TextInput(attrs={'type':'datetime-local'}))
    