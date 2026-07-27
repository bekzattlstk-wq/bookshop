# Китеп, магазин, издөө, жанр жана аккаунт барактарынын backend логикасына жооп берет.
# Функции для отображения шаблонов, поиска объектов и перенаправления пользователя.
from django.shortcuts import render, get_object_or_404, redirect
# Система одноразовых уведомлений Django.
from django.contrib import messages
# Функции входа и выхода пользователя из аккаунта.
from django.contrib.auth import login, logout
# Стандартная форма регистрации пользователя.
from django.contrib.auth.forms import UserCreationForm
# Декораторы, которые разрешают или запрещают доступ без авторизации.
from django.contrib.auth.decorators import login_required, login_not_required
# Объект Q позволяет объединять несколько условий поиска через OR или AND.
from django.db.models import Q
# Готовые классы Django для списка, просмотра, создания, изменения и удаления объектов.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Проверяет авторизацию пользователя в представлениях, созданных на основе классов.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
# Модель Article, из которой получаем города и статьи из базы данных.
from .models import Book, Category, Product, Genre
# Форма создания и редактирования статьи.
from .forms import BookForm, ProductForm
# Создаёт URL после успешного удаления объекта только в момент его использования.
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST


class StaffRequiredMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff


class ProductList(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'app/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return (
            Product.objects
            .filter(is_available=True)
            .select_related('category')
            .order_by('name')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'app/product_detail.html'
    context_object_name = 'product'

class ProductCreate(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'app/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductUpdate(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'app/product_form.html'
    context_object_name = 'product'
    success_url = reverse_lazy('product_list')

class ProductDelete(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Product
    template_name = 'app/product_confirm_delete.html'
    context_object_name = 'product'
    success_url = reverse_lazy('product_list')


@login_required
@require_POST
def delete_all_products(request):
    if not request.user.is_staff:
        raise PermissionDenied
    deleted_count = Product.objects.count()
    Product.objects.all().delete()
    messages.success(request, f'Удалено товаров: {deleted_count}.')
    return redirect('product_list')

class CategoryDetail(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'app/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['products'] = self.object.products.filter(
            is_available=True
        )

        return context


# Открывает главную страницу. Доступна только авторизованным пользователям.
@login_required
def home(request):
    # Передаёт все опубликованные книги, начиная с самой новой.
    books = Book.objects.filter(
        is_published=True,
    ).order_by('-created_at', '-id')

    return render(request, 'app/home.html', {'books': books})


@login_required
def new_books(request):
    # Отдельная страница с восемью последними опубликованными книгами.
    books = Book.objects.filter(
        is_published=True,
    ).order_by('-created_at', '-id')[:8]

    return render(request, 'app/new_books.html', {'books': books})


@login_required
def favorites_page(request):
    return render(request, 'app/favorites.html')


@login_required
def genre_books(request):
    genre_name = request.GET.get('name', '').strip()
    genre = get_object_or_404(Genre, name__iexact=genre_name)
    books = (
        Book.objects
        .filter(is_published=True, genres=genre)
        .prefetch_related('genres')
        .distinct()
        .order_by('-created_at', '-id')
    )
    return render(
        request,
        'app/genre_books.html',
        {'genre': genre, 'books': books},
    )


# Открывает вход на сайт: завершает текущую сессию и перенаправляет на страницу авторизации.
@login_not_required
def entry(request):
    # Выходит из текущего аккаунта, если пользователь был авторизован.
    logout(request)
    # Перенаправляет пользователя на URL с именем login.
    return redirect('login')

# Открывает страницу «О нас». Доступна только авторизованным пользователям.
@login_required
def about(request):
    # Создаёт список участников команды. Каждый словарь описывает одного сотрудника.
    team = [
        {
            'name': 'Айбек Асанов',
            'role': 'Team Lead / Backend',
            'bio': 'Проектирует архитектуру и создаёт надёжный backend на Django.',
            'icon': 'bi-code-square',
            'accent': 'accent-violet',
        },
    ]
    return render(request, 'app/about.html', {'team': team})

# Открывает страницу контактов. Доступна только авторизованным пользователям.
@login_required
def contact(request):
    # Отображает шаблон contact.html без дополнительных данных.
    return render(request, 'app/contact.html')


# Регистрирует нового пользователя. Страница доступна без авторизации.
@login_not_required
def register(request):
    # Если форма отправлена методом POST, обрабатываем введённые данные.
    if request.method == 'POST':
        # Создаёт форму и заполняет её данными, полученными от пользователя.
        form = UserCreationForm(request.POST)
        # Проверяет правильность логина, пароля и подтверждения пароля.
        if form.is_valid():
            # Сохраняет нового пользователя в базе данных.
            user = form.save()
            # Сразу авторизует зарегистрированного пользователя.
            login(request, user)
            # Создаёт приветственное уведомление, которое будет показано на следующей странице.
            messages.success(request, f'Добро пожаловать, {user.username}!')
            # После успешной регистрации перенаправляет на главную страницу.
            return redirect('home')
    else:
        # При обычном открытии страницы создаёт пустую форму регистрации.
        form = UserCreationForm()
    # Открывает register.html и передаёт в него форму через переменную form.
    return render(request, 'registration/register.html', {'form': form})

# Показывает список опубликованных статей.
class BookList(LoginRequiredMixin, ListView):
    # Указывает, с какой моделью работает представление.
    model = Book
    # Указывает HTML-шаблон страницы списка.
    template_name = 'app/book_list.html'
    # В шаблоне список объектов будет доступен под именем articles.
    context_object_name = 'books'

    # Определяет, какие записи будут показаны в списке.
    def get_queryset(self):
        # Возвращает только опубликованные статьи.
        return Book.objects.filter(is_published=True)

    # Добавляет дополнительные данные в контекст шаблона.
    def get_context_data(self, **kwargs):
        # Получает стандартный контекст, который создал ListView.
        context = super().get_context_data(**kwargs)
        # Преобразует QuerySet статей в обычный список Python.
        articles = list(context['books'])
        # Распределяет статьи по трём колонкам для отображения в шаблоне.
        context['book_columns'] = [articles[index::3] for index in range(3)]
        # Возвращает готовый контекст в article_list.html.
        return context


# Показывает полную информацию об одной статье.
class BookDetail(LoginRequiredMixin, DetailView):
    # Указывает модель, из которой будет найден объект.
    model = Book
    # Указывает шаблон страницы с полной информацией.
    template_name = 'app/book_detail.html'
    # В шаблоне текущая статья будет доступна под именем article.
    context_object_name = 'book'

    # Обрабатывает GET-запрос и сохраняет просмотренную статью в сессии.
    def get(self, request, *args, **kwargs):
        # Вызывает стандартный get(), который находит статью и создаёт ответ.
        response = super().get(request, *args, **kwargs)
        # Получает ID открытой статьи.
        book_id = self.object.id
        # Получает список ранее просмотренных статей из сессии.
        viewed_ids = request.session.get('recently_viewed_city_ids', [])
        # Удаляет текущий ID из старой позиции, чтобы не было повторений.
        viewed_ids = [
            saved_id for saved_id in viewed_ids
            if saved_id != book_id
        ]
        # Добавляет текущую статью в начало и хранит максимум три ID.
        request.session['recently_viewed_city_ids'] = [book_id, *viewed_ids][:3]
        # Возвращает пользователю сформированную HTML-страницу.
        return response

    # Добавляет в шаблон список всех опубликованных городов.
    def get_context_data(self, **kwargs):
        # Получает стандартный контекст DetailView.
        context = super().get_context_data(**kwargs)
        # Передаёт опубликованные статьи в переменную cities для рулетки городов.
        context['cities'] = Book.objects.filter(is_published=True)
        # Возвращает дополненный контекст в article_detail.html.
        return context


# Создаёт новую статью через форму. Требует авторизацию.
class BooksCreate(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    # Указывает модель создаваемого объекта.
    model = Book
    # Использует пользовательскую форму ArticleForm.
    form_class = BookForm
    # Открывает общий шаблон формы статьи.
    template_name = 'app/book_form.html'
    # Задаёт имя объекта в контексте шаблона.
    context_object_name = 'books'

    # Ограничивает набор объектов только опубликованными статьями.
    def get_queryset(self):
        return Book.objects.filter(is_published=True)



# Редактирует существующую статью через форму. Требует авторизацию.
class BookUpdate(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    # Указывает редактируемую модель.
    model = Book
    # Использует ту же форму, что и создание статьи.
    form_class = BookForm
    # Использует общий шаблон создания и редактирования.
    template_name = 'app/book_form.html'
    # Задаёт имя объекта в контексте шаблона.
    context_object_name = 'books'

    # Разрешает редактировать только опубликованные статьи.
    def get_queryset(self):
        return Book.objects.filter(is_published=True)




# Удаляет статью после подтверждения. Требует авторизацию.
class BookDelete(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    # Указывает удаляемую модель.
    model = Book
    # Открывает страницу подтверждения удаления.
    template_name = 'app/book_confirm_delete.html'
    # В шаблоне удаляемый объект доступен под именем article.
    context_object_name = 'book'
    # После удаления перенаправляет пользователя к списку статей.
    success_url = reverse_lazy('book_list')

    # Разрешает удалять только опубликованные статьи.
    def get_queryset(self):
        return Book.objects.filter(is_published=True)




# Ищет опубликованные статьи по заголовку или содержанию.
def search_books(request):
    # Получает поисковую строку из адреса вида /search/?q=текст.
    query = request.GET.get('q', '')
    # Сначала получает все опубликованные статьи.
    results = Book.objects.filter(is_published=True)
    # Если пользователь ввёл текст, фильтрует результаты поиска.
    if query:
        # Ищет совпадение без учёта регистра в title ИЛИ content.
        results = results.filter(Q(title__icontains=query) | Q(content__icontains=query))
    # Открывает search.html и передаёт найденные статьи и поисковый запрос.
    return render(request, 'app/search.html', {'results': results, 'query': query})
