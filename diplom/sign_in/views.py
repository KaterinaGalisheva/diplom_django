from django.shortcuts import render
from .models import CustomUser
from .forms import  RegistrationForm
from django.utils import timezone

import logging
# Создание базового логирования
logging.basicConfig(filename='errors.log', level=logging.INFO)



# Create your views here.
# функции для регистрации пользователей   
def sign_in(request):
    logging.info('Джанго. Пользователь начал регистрацию')
    info = {}
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            birthdate = form.cleaned_data['birthdate']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']


            # Проверка на совпадение паролей
            if password1 != password2:
                info['error'] = 'Пароли не совпадают'
                return render(request, 'sign_in/sign_in.html', {'info':info, 'form':form})
            # Проверка на совершеннолетие
            elif (timezone.now().date() - birthdate).days < 18 * 365:
                info['error'] = 'Вы несовершеннолетний'
                return render(request, 'sign_in/sign_in.html', {'info':info, 'form':form})
            # Проверка на существование пользователя
            elif CustomUser.objects.filter(username=username).exists():
                info['error'] = 'Такой пользователь уже существует'
                return render(request, 'sign_in/sign_in.html', {'info':info, 'form':form})
            else:
                # Создание пользователя
                user = CustomUser(username=username, birthdate=birthdate, email=email)
                user.set_password(password1)  # Хешируем пароль
                user.save()
                logging.info('Джанго. Пользователь сохранен')
                info['success'] = "Регистрация прошла успешно!"
                return render(request, 'sign_in/sign_in.html', {'info':info, 'form':form})
       
    else:
        form = RegistrationForm() 
    
    return render(request, 'sign_in/sign_in.html', {'info':info, 'form':form})


