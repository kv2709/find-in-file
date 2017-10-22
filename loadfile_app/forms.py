from django import forms
from .models import LoadFile

class LoadFileForm(forms.ModelForm):
    class Meta:
        model = LoadFile
        fields = ['file_obj'
                  ]





class StrInputForm(forms.ModelForm):
    class Meta:
        model = LoadFile
        fields = ['str_for_search',
                  ]
        labels = {'str_for_search': 'Строка для поиска',
                  }
        widgets = {'str_for_search': forms.TextInput(attrs={'size': 80}),
                   }

