from django import forms
from .models import Gallery,Image
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password=forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label='Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['email'].label='Электороная почта'
        self.fields['confirm_password'].label='Подтвердите пароль'
        
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(f'Данный e-mail уже зарегистрован')
        return self.cleaned_data['email']

    def clean_username(self):
        username= self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Имя {username} занято')
        return username
    
    def clean(self):
        password = self.cleaned_data['password']
        confirm_password= self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    class Meta:
        model=User
        fields=['username','email','password','confirm_password',]
        

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label='Логин или е-майл'
        self.fields['password'].label = 'Пароль'
        
    def clean(self):
        username= self.cleaned_data['username']
        password= self.cleaned_data['password']
        if '@' in username:
            if not User.objects.filter(email=username).exists():
                raise forms.ValidationError(f'Пользователь с  почтой  {username} не найден.')
        else:
            if not User.objects.filter(username=username).exists():
                raise forms.ValidationError(f'Пользователь с логином   {username} не найден.')

        user = User.objects.filter(username=username).first()
        user1= User.objects.filter(email=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError("Неверный пароль")
        else:
            if not user1.check_password(password):
                raise forms.ValidationError("Неверный пароль")
        return self.cleaned_data
    
    class Meta:
        model=User
        fields= ['username','password']







class NewImageForm(forms.ModelForm):
    
    CHOICES = (('Option 1', 'Сохранить оригинал'),
                ('Option 2', 'Сохранить квадратом'),
                ('Option 3', 'Сохранить уменьшеную 256*256'),
                ('Option 4', 'Сохранить все варианты'),)

    title = forms.CharField(max_length=100,label='Название галлереи')
    field = forms.ChoiceField(choices=CHOICES,label='Выберите Действие ')

    class Meta:
        model=Image
        fields =['title','picture','field']