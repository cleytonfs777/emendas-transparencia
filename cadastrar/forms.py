from django import forms


class ViaturaFilterForm(forms.Form):
    search_titular = forms.CharField(
        label='Filtrar por Titular', required=False)
