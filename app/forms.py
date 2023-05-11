from django import forms

from .models import Tours, Favourite, TourImage
from django.forms import DateInput

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
import re
from django.core.exceptions import ValidationError

# Объявляем переменную отвечающую за значение количества товара
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

# форма добавления товара в корзину
class CartAddProductForm(forms.Form):
    # # Поле для выбора количества товара
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    # Флаг обновления количества товара в корзине
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
#
class CartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        label='Количество',
        initial=1,
        widget=forms.NumberInput(
            attrs={'class': 'form-control',
                   'style': 'width: 100px; display: inline-block;'}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)



class CustomDateInput(DateInput):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['type'] = 'date'
        attrs['class'] = 'form-control'
        attrs['use_required_attribute'] = True # добавляем нужный атрибут
        super().__init__(attrs)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label = 'Пароль',
        widget = forms.PasswordInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Пароль',
        }))
    password2 = forms.CharField(
        label = 'Повторите пароль',
        widget = forms.PasswordInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
        }))
    username = forms.CharField(
        label = 'Логин ',
        widget = forms.TextInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Логин пользователя', }),
        min_length = 2)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    last_name = forms.CharField(
        label = 'Фамилия',
        widget = forms.TextInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Фамилия', }),)
    first_name = forms.CharField(
        label = 'Имя',
        widget = forms.TextInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Имя', }),)
    email = forms.CharField(
        label = 'Эл. почта',
        widget = forms.TextInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Электронная почта', }),)

    def clean_username(self):
        username = self.cleaned_data['username']
        if re.match(r'\d', username):
            raise ValidationError('Поле не должно начинаться с цифры')
        return username

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label = 'Логин пользователя',
        widget = forms.TextInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Логин'}),
        min_length = 2)
    password = forms.CharField(
        label = 'Ваш пароль ',
        widget = forms.PasswordInput(), )


class ToursForm(forms.ModelForm):
    additional_images = forms.ImageField(widget = forms.ClearableFileInput(attrs = {'multiple': True}),
                                         required = False)
    class Meta:
        model = Tours
        fields = ('name', 'description', 'price', 'photo', 'exist', 'category')

        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Название тура'
                }
            ),
            'description': forms.Textarea(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Описание тура'
                }
            ),
            'price': forms.NumberInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Стоимость тура'
                }
            ),

            'photo': forms.ClearableFileInput(
                attrs = {
                    'class': 'form-control-file'
                }
            ),
            'exist': forms.CheckboxInput(
                attrs = {
                    'class': 'form-check-input',

                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if re.match(r'\d', name):
            raise ValidationError('Поле не должно начинаться с цифры')
        return name

    def save(self, commit=True):
        instance = super().save(commit = False)
        instance.save()

        for img in self.files.getlist('additional_images'):
            tour_image = TourImage(tour = instance)
            tour_image.image.save(img.name, img)
            tour_image.save()

        return instance

class FavouriteAddForm(forms.ModelForm):
    class Meta:
        model = Favourite
        fields = []

class ContactForm(forms.Form):
    subject = forms.CharField(
        label='Укажите вкратце тему обращения',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    content = forms.CharField(
        label='Напишите здесь ваш вопрос\предложение',
        widget=forms.Textarea(
            attrs={'class': 'form-control',
                   'rows': 5, }
        )
    )
