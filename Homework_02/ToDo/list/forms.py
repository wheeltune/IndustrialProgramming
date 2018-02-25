from django import forms

class AddFrom(forms.Form):
    content = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'placeholder':'Название'}))
    deadline = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'], widget=forms.TextInput(attrs={'type':'datetime-local'}))
    
class RemoveForm(forms.Form):
    id = forms.IntegerField(widget=forms.TextInput(attrs={'type':'hidden'}))

class MarkDoneForm(forms.Form):
    id = forms.IntegerField(widget=forms.TextInput(attrs={'type':'hidden'}))
    is_done = forms.BooleanField(widget=forms.CheckboxInput(attrs={'onclick':'this.form.submit();'}))