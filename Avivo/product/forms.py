from cProfile import label
from tkinter import Widget
from django import forms

from .models import Product, Comment


class ProductForm(forms.ModelForm):
    max_size_image = 7

    class Meta:
        model = Product
        fields = ('image', 'description')
        labels = {
            'description': 'Описание',
            'image': 'Фотография'
        }
        Widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание'
            })
        }

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > self.max_size_image*1024*1024:
                raise forms.ValidationError((f'Файл должен быть меньше'
                                             f'{self.max_size_image} МБ'))
            return image
        else:
            raise forms.ValidationError('Не удалось прочитать файл')

