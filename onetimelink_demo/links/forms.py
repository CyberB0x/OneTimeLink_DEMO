from django import forms
from .models import OneTimeLink

EXPIRATION_CHOICES = [
    (1, '1 min'),
    (2, '2 min'),
    (5, '5 min'),
]

class OneTimeLinkForm(forms.ModelForm):
    expiration_minutes = forms.TypedChoiceField(
        choices=EXPIRATION_CHOICES,
        coerce=int,
        label='Link Lifetime'
    )

    class Meta:
        model = OneTimeLink
        fields = ['file', 'text', 'expiration_minutes']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file and file.size > 10 * 1024 * 1024:  # 10 МБ
            raise forms.ValidationError("The maximum file size is 10 MB.")
        return file

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('file') and not cleaned_data.get('text'):
            raise forms.ValidationError("You need to upload a file or enter text.")
        return cleaned_data


class AccessLinkForm(forms.Form):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль (если есть)'}),
        label='Пароль'
    )