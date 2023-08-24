from django.shortcuts import render
from .models import Posts, Theme
from .forms import PostsForm
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils import timezone

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

# Отображение главной старницы
def index(request):

    data = {
        'db': None,
        'theme': None
    }

    selectTheme(request, data)

    # AJAX запрос
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'POST':
            # Смена темы
            switchTheme(request)
            return JsonResponse(data)
        else:
            pass

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

        else:
            pass

    # Добавляется бд с постами в словарь data
    db = Posts.objects.order_by('-date')
    data['db'] = db

    return render(request, 'main/index.html', data)

# Отображение главной старницы при поиске
def indexSearch(request, search):

    data = {
        'db': None,
        'theme': None
    }

    selectTheme(request, data)

    # AJAX запрос
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'POST':
            # Смена темы
            switchTheme(request)
            return JsonResponse(data)
        else:
            pass

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

        else:
            pass

    # Добавляется бд с постами в словарь data
    db = Posts.objects.order_by('-date')
    data['db'] = db

    # Переменная пустой базы данных для добавления в неё найденных постов
    searchDB = Posts.objects.none()

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

    return render(request, 'main/index.html', data)

# Отображение страницы "Подробнее о блоге"
def about(request):
    data = {
        'theme': None
    }

    selectTheme(request, data)

    # AJAX запрос
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'POST':
            # Смена темы
            switchTheme(request)
            return JsonResponse(data)
        else:
            pass

    return render(request, 'main/about.html', data)

# Отображение страницы "Добавить пост"
def addPost(request):
    error = ''
    data = {
        'form': None,
        'error': error,
        'theme': None
    }

    selectTheme(request, data)

    # AJAX запрос
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'POST':
            # Смена темы
            switchTheme(request)
            return JsonResponse(data)

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
            pass
        
    data['form'] = PostsForm()

    return render(request, 'main/addEditPost.html', data)

# Отображение страницы с полным содержанием поста
def fullArticle(request, id):
    data = {
        'post': None,
        'theme': None,
    }

    selectTheme(request, data)

    # AJAX запрос
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'POST':
            # Смена темы
            switchTheme(request)
            return JsonResponse(data)
        else:
            pass

    if request.method == 'POST':
        # Проверка на тип запроса
        requestType = request.POST
        keys = []
        for k in requestType:
            keys.append(k)
        requestType = keys[1]

        print(requestType)

        # Кнопка добавления поста
        if requestType == 'deletePost':

            deletedPost = Posts.objects.get(id=id)
            deletedPost.delete()

            return redirect('/')
   
        else:
            pass

    selectTheme(request, data)

    data['post'] = Posts.objects.filter(id=id)
    return render(request, 'main/fullArticle.html', data)

# Отображение страницы "Редактирование поста"
def editPost(request, id):
    data = {
        'id': id,
        'form': None,
        'theme': None,
        'post': None
    }
    selectTheme(request, data)

    # AJAX запрос
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'POST':
            # Смена темы
            switchTheme(request)
            return JsonResponse(data)

    post = Posts.objects.get(id=id)
    data['post'] = post
    data['form'] = PostsForm(instance=post)

    if request.method == 'POST':
        # Проверка на тип запроса
        requestType = request.POST
        keys = []
        for k in requestType:
            keys.append(k)
        requestType = keys[1]

        # Кнопка редактированя поста
        if requestType == 'title':
            form = PostsForm(request.POST, instance=post)

            post = Posts.objects.all()
            print(timezone.now())

            if form.is_valid():
                form.save() # Сохранение формы

                # Добавление даты изменения в бд
                update = post.get(id=id)
                update.editDate = timezone.now()
                update.save()

                return redirect('/')

    return render(request, 'main/addEditPost.html', data)