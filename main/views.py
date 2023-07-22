from django.shortcuts import render
from .models import Posts, Theme
from .forms import PostsForm
from django.shortcuts import redirect
from django.urls import reverse

# My Functions

# Функция выбора темы по ip пользователя
def selectTheme(request, data):
    ipUser = request.META.get('REMOTE_ADDR')
    themesModel = Theme.objects.all()
    newUser = True

    for user in themesModel:
        if user.ip == ipUser:
            newUser = False
            selectedTheme = user.theme
            data['theme'] = selectedTheme
            break
        else:
            pass

    if newUser == True:
        themesModel.create(ip=ipUser, theme='light')
        data['theme'] = 'light'
    else:
        pass

# Функция переключения темы
def switchTheme(request):
    ipUser = request.META.get('REMOTE_ADDR')
    themesModel = Theme.objects.all()

    for user in themesModel:
        if user.ip == ipUser:
            selectedTheme = user.theme
            if selectedTheme == 'light':
                update = themesModel.get(ip=ipUser)
                update.theme = 'dark'
                update.save()
            else:
                update = themesModel.get(ip=ipUser)
                update.theme = 'light'
                update.save()
                
        else:
            pass


# Create your views here.

def index(request):

    data = {
        'db': None,
        'theme': None
    }

    db = Posts.objects.order_by('-date')
    searchDB = Posts.objects.none()
    data['db'] = db

    if request.method == 'POST':
        # Проверка на тип запроса
        requestType = request.POST
        keys = []
        for k in requestType:
            keys.append(k)
        requestType = keys[1]

        # Вывод постов из бд при поиске
        if requestType == 'searchText':
            search = request.POST.get('searchText')
            if search == '':
                return redirect('/')
            else:
                return redirect(f'/search={search}/')

        # Кнопка смены темы
        elif requestType == 'switchTheme':
            switchTheme(request)
            return redirect('/')

        else:
            pass

    selectTheme(request, data)
    return render(request, 'main/index.html', data)


def indexSearch(request, search):

    data = {
        'db': None,
        'theme': None
    }

    db = Posts.objects.order_by('-date')
    searchDB = Posts.objects.none()
    data['db'] = db

    
    searchByWords = search.split()
    for searchWord in searchByWords:
        for el in db:
            titleByWords = el.title.split()
            for word in titleByWords:
                if word.lower() == searchWord.lower():
                    db = Posts.objects.filter(title=el.title)
                    searchDB |= db
                else:
                    pass
    data['db'] = searchDB.order_by('-date')

    if request.method == 'POST':
        # Проверка на тип запроса
        requestType = request.POST
        keys = []
        for k in requestType:
            keys.append(k)
        requestType = keys[1]

        # Вывод постов из бд при поиске
        if requestType == 'searchText':
            search = request.POST.get('searchText')
            if search == '':
                return redirect('/')
            else:
                return redirect(f'/search={search}/')


        # Кнопка смены темы
        elif requestType == 'switchTheme':
            switchTheme(request)
            return redirect(f'/search={search}/')

        else:
            pass

    selectTheme(request, data)
    return render(request, 'main/index.html', data)


def about(request):
    data = {
        'theme': None
    }

    if request.method == 'POST':
        # Проверка на тип запроса
        requestType = request.POST
        keys = []
        for k in requestType:
            keys.append(k)
        requestType = keys[1]

        # Кнопка смены темы
        if requestType == 'switchTheme':
            switchTheme(request)
            return redirect('/about/')
    
    selectTheme(request, data)
    return render(request, 'main/about.html', data)


def addarticle(request):
    error = ''
    form = PostsForm()
    data = {
        'form': form,
        'error': error,
        'theme': None
    }

    if request.method == 'POST':
        # Проверка на тип запроса
        requestType = request.POST
        keys = []
        for k in requestType:
            keys.append(k)
        requestType = keys[1]

        # Кнопка добавления поста
        if requestType == 'title':
            form = PostsForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')
            else:
                error = 'Форма заполнена неверно'

        # Кнопка смены темы
        elif requestType == 'switchTheme':
            switchTheme(request)
            return redirect('/addarticle/')

    selectTheme(request, data)
    return render(request, 'main/addarticle.html', data)


def fullArticle(request, id):
    db = Posts.objects.filter(id=id)

    data = {
        'db': db,
        'theme': None
    }

    if request.method == 'POST':
        # Проверка на тип запроса
        requestType = request.POST
        keys = []
        for k in requestType:
            keys.append(k)
        requestType = keys[1]

        # Кнопка смены темы
        if requestType == 'switchTheme':
            switchTheme(request)
            return redirect(f'/post{id}')

    selectTheme(request, data)
    return render(request, 'main/fullArticle.html', data)
