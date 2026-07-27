# Китеп жана товар кошуу/редакциялоо формаларынын талааларына жана көрүнүшүнө жооп берет.
from django import forms
from .models import Book, Product

class BookForm(forms.ModelForm):
    class Meta:
        model = Book

        fields = ['title',
                  'slug',
                  'content',
                  'genres',
                  'image',
                  'is_published']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-custom',
                                            'placeholder': 'Введите название книги'}),

            'slug': forms.TextInput(attrs={'class': 'form-control form-control-custom',
                                           'placeholder': 'ведите URL, например: moyi knigi'}),

            'content': forms.Textarea(attrs={'class': 'form-control form-control-custom',
                                             'placeholder': 'Введите описание книги'}),

            'genres': forms.CheckboxSelectMultiple(),

            'image': forms.FileInput(attrs={'class': 'form-control'}),

            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError('Имя книги должен содержать минимум 5 символов')
        return title



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product

        fields = [
            'name',
            'slug',
            'category',
            'price',
            'description',
            'image',
            'is_available',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название товара',
            }),

            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: kniga-dzhamilya',
            }),

            'category': forms.Select(attrs={
                'class': 'form-control',
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите цену',
                'min': '0',
                'step': '0.01',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание товара',
            }),

            'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),

            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
