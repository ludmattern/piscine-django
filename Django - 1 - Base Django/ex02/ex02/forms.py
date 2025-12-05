from django import forms


class InputForm(forms.Form):
    """Formulaire avec un champ de texte."""
    text = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Entrez votre texte...',
            'class': 'form-input'
        })
    )
