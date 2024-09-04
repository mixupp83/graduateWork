# Дипломная работа 
___
## TEMA: Разработать простые веб-приложения с использованием Django, Flask и FastAPI, провести их сравнение.
### Автор: Вереин Михаил Павлович
___
__Оглавление дипломной работы:__
1. Введение
2. Цель и задачи
3. Методология
4. Разработка приложений
5. Сравнение фреймворков
6. Заключение
7. Список литературы
___
## 1. Введение

В современном мире веб-разработки существует множество фреймворков, каждый из которых имеет свои особенности и
преимущества. В данной дипломной работе будет проведено сравнение трех популярных Python-фреймворков: Django, Flask и
FastAPI. Целью работы является анализ и сравнение этих фреймворков с точки зрения их использования для разработки простых
веб-приложений.

## 2. Цель и задачи

  Цель работы: Провести анализ и сравнение трех Python-фреймворков (Django, Flask, FastAPI) для разработки простых веб-приложений.
Задачи:
Изучить особенности и преимущества каждого из фреймворков.
Разработать простые веб-приложения с использованием Django, Flask и FastAPI.
Провести сравнение фреймворков по различным критериям: производительность, простота использования, гибкость, документация и сообщество.
Сделать выводы о наиболее подходящем фреймворке для различных типов проектов.

## 3. Методология

Исследование литературы и ресурсов: Изучение документации, статей, блогов и других источников информации о Django, Flask и FastAPI.
Разработка приложений: Создание простых веб-приложений с использованием каждого из фреймворков.
Тестирование и сравнение: Проведение тестов для оценки производительности, простоты использования и других критериев.
Анализ результатов: Сравнение результатов и формулирование выводов.

## 4. Разработка приложений

* [Django](https://github.com/mixupp83/graduateWork/tree/master/graduate_django/graduate_project)

### *Описание проекта:* 

Создание простого блога с функционалом добавления, редактирования и удаления статей.

Проект представляет собой простой блог, разработанный с использованием фреймворка Django. Основные функции включают 
создание, редактирование, просмотр и удаление статей. Приложение также включает административный интерфейс для 
управления контентом.

### *Структура проекта:*

Проект состоит из следующих основных компонентов:
* Модели (models.py): Определение модели Article, которая содержит поля title, content и pub_date.
* Формы (forms.py): Определение формы ArticleForm для создания и редактирования статей.
* Представления (views.py): Обработка запросов и управление логикой приложения.
* Шаблоны (templates/myapp): HTML-шаблоны для отображения списка статей, деталей статьи, формы редактирования и подтверждения удаления.
* Административная панель (admin.py): Настройка административного интерфейса для управления статьями.

### *Детали реализации*

*Модели (models.py)*
```python
class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование')
    content = models.TextField(verbose_name='Содержание (контент)')
    pub_date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')

    def __str__(self):
        return self.title
```
Модель Article содержит следующие поля:
* title: Заголовок статьи (CharField).
* content: Содержание статьи (TextField).
* pub_date: Дата публикации статьи (DateTimeField).

*Формы (forms.py)*
```python
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
```
Форма ArticleForm используется для создания и редактирования статей. Она наследуется от forms.ModelForm и определяет 
модель Article и поля title и content.

*Представления (views.py)*
```python
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'myapp/article_list.html', {'articles': articles})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'myapp/article_detail.html', {'article': article})

def article_new(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'myapp/article_edit.html', {'form': form})

def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'myapp/article_edit.html', {'form': form})

def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        article.delete()
        return redirect('article_list')
    return render(request, 'myapp/article_confirm_delete.html', {'article': article})
```
* article_list: Отображает список всех статей.
* article_detail: Отображает детали конкретной статьи.
* article_new: Создает новую статью.
* article_edit: Редактирует существующую статью.
* article_delete: Удаляет статью после подтверждения.

*Шаблоны (templates/myapp)*
* article_list.html: Отображает список всех статей.
```html
    <h2>Список статей</h2>
    <ul>
        {% for article in articles %}
            <li>
                <a href="{% url 'article_detail' article.pk %}">{{ article.title }}</a>
                <a href="{% url 'article_edit' article.pk %}">Редактировать</a>
                <a href="{% url 'article_delete' article.pk %}">Удалить</a>
            </li>
        {% endfor %}
    </ul>
```
* article_detail.html: Отображает детали конкретной статьи.
```html
{% block content %}
    <h2>{{ article.title }}</h2>
    <p>{{ article.content }}</p>
    <p>Опубликовано: {{ article.pub_date }}</p>
    <a href="{% url 'article_edit' article.pk %}">Редактировать</a>
    <a href="{% url 'article_delete' article.pk %}">Удалить</a>
    <a href="{% url 'article_list' %}">Вернуться к списку</a>
{% endblock %}
```
* article_edit.html: Форма для создания и редактирования статей.
```html
{% block content %}
    <h2>Редактировать статью</h2>
    <form method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Сохранить</button>
    </form>
    <a href="{% url 'article_list' %}">Вернуться к списку</a>
{% endblock %}
```
* article_confirm_delete.html: Форма подтверждения удаления статьи.
```html
{% block content %}
    <h2>Вы уверены, что хотите удалить "{{ article.title }}"?</h2>
    <form method="POST">
        {% csrf_token %}
        <button type="submit">Да, удалить</button>
    </form>
    <a href="{% url 'article_detail' article.pk %}">Отмена</a>
{% endblock %}
```
* Административная панель (admin.py)
```python
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'content')
    list_filter = ('pub_date',)
    search_fields = ('title', 'content')

admin.site.register(Article, ArticleAdmin)
```
Настроена административная панель для управления статьями. Определен класс ArticleAdmin, который настраивает отображение
списка статей, фильтрацию по дате публикации и поиск по заголовку и содержанию.

![img.png](img.png)

### *Примеры работы*
Список статей

![Список статей](img_1.png)

Детали статьи

![Детали статьи](img_2.png)

Форма редактирования статьи

![Форма редактирования статьи](img_3.png)

Форма подтверждения удаления статьи

![Форма подтверждения удаления статьи](img_4.png)

* [Flask](https://github.com/mixupp83/graduateWork/tree/master/graduate_flask)
### *Описание проекта:* 
    
Проект представляет собой простое веб-приложение для управления списком задач (To-Do List), разработанное с использованием
фреймворка Flask и базы данных SQLite. Основные функции включают создание, редактирование, просмотр, завершение и удаление 
задач.

### *Структура проекта*
Проект состоит из следующих основных компонентов:
* Модели (models.py): Определение модели Task, которая содержит поля id, title, description и completed.
* Представления (views.py): Обработка запросов и управление логикой приложения.
* Шаблоны (templates): HTML-шаблоны для отображения списка задач, деталей задачи, формы редактирования и подтверждения удаления.
* База данных (tasks.db): SQLite база данных для хранения задач.

### *Детали реализации*
* Модели (models.py)
```python

```
Модель Task содержит следующие поля:
* id: Уникальный идентификатор задачи (Integer, primary_key).
* title: Заголовок задачи (String).
* description: Описание задачи (Text).
* completed: Флаг завершения задачи (Boolean, default=False).

Представления (views.py)
task_list: Отображает список всех задач.

task_detail: Отображает детали конкретной задачи.

task_new: Создает новую задачу.

task_edit: Редактирует существующую задачу.

task_complete: Переключает статус завершения задачи.

task_delete: Удаляет задачу после подтверждения.

Шаблоны (templates)
task_list.html: Отображает список всех задач.

task_detail.html: Отображает детали конкретной задачи.

task_edit.html: Форма для создания и редактирования задач.

База данных (tasks.db)
База данных SQLite используется для хранения задач. При запуске приложения создается файл tasks.db, если он не существует.

Установка и запуск
Установите зависимости:

bash
Copy code
pip install Flask Flask-SQLAlchemy
Запустите приложение:

bash
Copy code
python app.py
Откройте браузер и перейдите по адресу http://127.0.0.1:5000/ для просмотра списка задач.

Примеры работы
Список задач
Список задач

Детали задачи
Детали задачи

Форма редактирования задачи
Форма редактирования задачи

Форма подтверждения удаления задачи
Форма подтверждения удаления задачи

Личный кабинет
Для добавления функционала личного кабинета можно использовать встроенные механизмы аутентификации Flask. Создайте представления и шаблоны для регистрации, входа и управления профилем пользователя.

Презентабельный и удобный интерфейс
Для улучшения пользовательского опыта можно использовать современные фронтенд-технологии и фреймворки, такие как Bootstrap или Tailwind CSS. Добавьте стили и JavaScript для улучшения внешнего вида и функциональности интерфейса.

Автор: Вереин Михаил Павлович

Контактная информация: [email protected]

* [FastAPI](https://github.com/mixupp83/graduateWork/tree/master/graduate_fastapi)
  * Описание проекта: 
    * Создание простого API для управления книгами в библиотеке.
  * Технические детали:
    * Использование FastAPI для создания маршрутов и обработки запросов.
    * Работа с базой данных через SQLAlchemy.
    * Использование Pydantic для валидации данных.

__5. Сравнение фреймворков__

* Производительность:
  * Django: Хорошая производительность, но может быть избыточен для небольших проектов.
  * Flask: Легковесный и быстрый, подходит для небольших и средних проектов.
  * FastAPI: Высокая производительность, особенно хорош для API и асинхронных задач.
* Простота использования:
  * Django: Богатый функционал, но требует более глубокого изучения.
  * Flask: Простой и гибкий, легко начать использовать.
  * FastAPI: Простой синтаксис, автоматическая генерация документации.
* Гибкость:
  * Django: Большая структура, менее гибкий для нестандартных решений.
  * Flask: Высокая гибкость, позволяет строить приложение по своему усмотрению.
  * FastAPI: Гибкий, но требует более глубокого понимания асинхронного программирования.
* Документация и сообщество:
  * Django: Широкая документация и большое сообщество.
  * Flask: Хорошая документация и активное сообщество.
  * FastAPI: Хорошая документация, но сообщество меньше по сравнению с Django и Flask.

Выводы:
Django подходит для крупных проектов с большим количеством функционала и требований к безопасности.
Flask идеально подходит для небольших и средних проектов, где требуется гибкость и простота.
FastAPI отлично подходит для разработки API с высокой производительностью и асинхронными задачами.

__6. Заключение__

В данной дипломной работе было проведено сравнение трех популярных Python-фреймворков: Django, Flask и FastAPI. Каждый из них имеет свои преимущества и подходит для различных типов проектов.
Выбор фреймворка зависит от конкретных требований проекта, его масштаба и специфики. Например мы можем использовать FastAPI из-за его высокой производительности при разработке API, Flask можно использовать для создания малых и средних проектов с большой гибкостью, а Django — для создания многофункциональных крупномасштабных приложений.

__7. Список литературы__

* [Django Documentation.](https://docs.djangoproject.com/)
* [Flask Documentation.](https://flask.palletsprojects.com/)
* [FastAPI Documentation.](https://fastapi.tiangolo.com/)
* "Django vs Flask vs FastAPI: A Comprehensive Comparison" - Blog post by Towards Data Science.
* "Choosing the Right Python Web Framework" - Article by Real Python.

__Приложение:__

Исходный код разработанных приложений на [Django](https://github.com/mixupp83/graduateWork/tree/master/graduate_django/graduate_project),
[Flask](https://github.com/mixupp83/graduateWork/tree/master/graduate_flask) и 
[FastAPI](https://github.com/mixupp83/graduateWork/tree/master/graduate_fastapi)
