from .models import *
from .forms import *
from django.shortcuts import render
from django.views.generic import DetailView,View,ListView,UpdateView,CreateView
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate,login


class IndexView(ListView):
    model=Gallery
    context_object_name = 'galleryes'
    template_name = 'index.html'
    extra_context={'title':'Главная страница'}  


class GalleryDetail(DetailView):
    model = Gallery
    context_object_name='gallery'
    template_name='gallery_detail.html'


class RegistrationView(View):
    def get(self,request,*args,**kwargs):
        if  request.user.is_authenticated:
            return redirect('index')
        form=RegistrationForm(request.POST or None)
        title = 'Регистрация'
        context = {
            'title':title,
            'form':form,
        }
        return render(request,'registration.html',context)

    def post(self,request,*args,**kwargs):
        form= RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user=form.save(commit=False)
            new_user.username=form.cleaned_data['username']
            new_user.email=form.cleaned_data['email']
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            user= authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            Profile.objects.create(user=user)
            login(request,user)
            return redirect('home')
        context={'form':form,}
        return render(request,'registration.html',context)


class LoginView(View):
    def get(self,request,*args,**kwargs):
        if  request.user.is_authenticated:
            return redirect('home')
        form = LoginForm(request.POST or None)
        title = 'Логин'
        context= {'title':title,
        'form':form,
        }
        return render(request,'login.html',context)

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST or None)
        if form.is_valid():
            username= form.cleaned_data['username']
            password = form.cleaned_data['password']
            if '@' in username:
                user1= User.objects.filter(email=username).first()
                user= authenticate(username=user1,password=password)
            else:
                user= authenticate(username=username,password=password)
            if user:
                Profile.objects.get_or_create(user=user)
                login(request,user)
            return HttpResponseRedirect('/')
        context={'form':form,}
        return render(request,'login.html',context)


class ProfileView(View):
    def get (self,request,*args,**kwargs):
        if not  request.user.is_authenticated:
            return redirect('registration')
        profile = Profile.objects.get(user=request.user)
        return render(request,'profile.html',{
                    'profile': profile
                    })


class NewImage(CreateView):
    model = Image
    form_class = NewImageForm
    template_name='create_image.html'
    extra_context={'title':'Сохранить фото'}  

    def form_valid(self,form):
        test = form.save(commit=False)
        image= self.request.FILES['picture']
        choice = form.cleaned_data.get("field")

        if len(image) == 0:
            raise form.ValidationError(u'Not found uploaded photos')

        gallery = Gallery.objects.create(title=form.cleaned_data.get("title"),owner=Profile.objects.get(user=self.request.user))
        if choice == 'Option 1':
            variant=Image.objects.create(picture=image)
            gallery.images.add(variant)
        if choice == 'Option 2':
            settings.DJANGORESIZED_DEFAULT_SIZE[0]=500
            settings.DJANGORESIZED_DEFAULT_SIZE[1]=500
            variable2=Image.objects.create(picture=image)
            gallery.images.add(variable2)
        if choice == 'Option 3':
            settings.DJANGORESIZED_DEFAULT_SIZE[0]=256
            settings.DJANGORESIZED_DEFAULT_SIZE[1]=256
            variant3=Image.objects.create(picture=image)
            gallery.images.add(variant3)
        if choice == 'Option 4':
            var1=Image.objects.create(picture=image)
            gallery.images.add(var1)
            settings.DJANGORESIZED_DEFAULT_SIZE[0]=500
            settings.DJANGORESIZED_DEFAULT_SIZE[1]=500
            var2=Image.objects.create(picture=image)
            gallery.images.add(var2)
            settings.DJANGORESIZED_DEFAULT_SIZE[0]=256
            settings.DJANGORESIZED_DEFAULT_SIZE[1]=256
            var3=Image.objects.create(picture=image)
            gallery.images.add(var3)



        return redirect('/')