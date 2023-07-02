from django import forms
from .models import AbvUser, SubRubric, SuperRubric, Bb, AdditionalImage, Comment
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.forms import  inlineformset_factory
from captcha.fields import CaptchaField
#Форма смены пароля
class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Ваш e-mail')
    class Meta:
        model = AbvUser
        fields = ('username','email','first_name','last_name','send_messages')

#Форма регистрации нового пользователя
class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Ваш e-mail')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput,
                                help_text='Повторите пароль')
    def clean_password(self):#Валидация пароля 1
        password1 = self.cleaned_data["password1"]
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):#Очистить форму если пароли не совпадают
        super().clean()
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1 != password2:
            errors = {'password2':ValidationError('Введеные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        user.is_activated = True
        if commit:
            user.save()
            return user
    class Meta:
        model = AbvUser
        fields = ('username','email','password1','password2','first_name','last_name','send_messages')

#Форма подрубрик
class SubRubricForm(forms.ModelForm):
    super_rubric = forms.ModelChoiceField(queryset=SuperRubric.object.all(), empty_label=None, label='Надрубрика', required=True)

    class Meta:
        model = SubRubric
        fields ='__all__'

#Форма поиск на сайте
class SeachForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=30, widget=forms.PasswordInput(attrs={'placeholder':'Поиск'}))

#Форма изменения объявления
class BbForm(forms.ModelForm):
    class Meta:
        model = Bb
        fields = '__all__'
        widgets = {'autor': forms.HiddenInput}

AIFormSet = inlineformset_factory(Bb, AdditionalImage, fields='__all__')

#Форма для комментарий для зарегистрированных пользователей
class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'bb':forms.HiddenInput}

#Формы для комментарий для незарегистрированных пользователей
class GuesCommentForm(forms.ModelForm):
    captcha = CaptchaField(label='Введите текст с картинки', error_messages={'invalid':'Неправильный текст'})
    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'bb':forms.HiddenInput}
