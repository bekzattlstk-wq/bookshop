# Долбоордун бардык негизги URL маршруттарын жана admin/allauth жолдорун бириктирет.
# Импортирует стандартную административную панель Django.
from django.contrib import admin
# Импортирует функцию создания URL-маршрутов.
from django.urls import path, include
# Подключает готовые представления для входа и выхода пользователя.
from django.contrib.auth import views as auth_views
# Получает настройки проекта для подключения медиафайлов.
from django.conf import settings
# Создаёт временные маршруты для медиафайлов в режиме разработки.
from django.conf.urls.static import static
# Импортирует представления основного приложения.
from app import views

# Содержит все основные URL-маршруты проекта.
urlpatterns = [
path(
    'products/',
    views.ProductList.as_view(),
    name='product_list'
),

# Жаңы товар
path(
    'product/create/',
    views.ProductCreate.as_view(),
    name='product_create'
),

path(
    'products/delete-all/',
    views.delete_all_products,
    name='products_delete_all'
),

# Бир товар
path(
    'product/<slug:slug>/',
    views.ProductDetail.as_view(),
    name='product_detail'
),

# Товарды оңдоо
path(
    'product/<slug:slug>/update/',
    views.ProductUpdate.as_view(),
    name='product_update'
),

# Товарды өчүрүү
path(
    'product/<slug:slug>/delete/',
    views.ProductDelete.as_view(),
    name='product_delete'
),

# Категориядагы товарлар
path(
    'category/<slug:slug>/',
    views.CategoryDetail.as_view(),
    name='category_detail'
),
    # Открывает административную панель Django.
    path('admin/', admin.site.urls),

    path('account/', include('allauth.urls')),

    # Перенаправляет посетителя на страницу входа.
    path('', views.entry, name='entry'),

    # Показывает стандартную форму авторизации в указанном шаблоне.
    path(
        'login/',auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login'
    ),

    # Завершает сеанс пользователя и возвращает его на страницу входа.
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # Открывает регистрацию нового пользователя.
    path('register/', views.register, name='register'),
    # Открывает главную страницу после авторизации.
    path('home/', views.home, name='home'),
    # Показывает восемь последних опубликованных книг на отдельной странице.
    path('new-books/', views.new_books, name='new_books'),
    path('favorites/', views.favorites_page, name='favorites'),
    path('genres/books/', views.genre_books, name='genre_books'),
    # Открывает страницу с информацией о проекте.
    path('about/', views.about, name='about'),
    # Открывает страницу контактов.
    path('contact/', views.contact, name='contact'),
    # Открывает личный профиль пользователя.
    #path('profile/', views.profile, name='profile'),


    # ===== ПОИСК =====
    # Показывает список опубликованных статей.
    path('books/', views.BookList.as_view(), name='book_list'),

    # ===== СТАТЬИ (CRUD) =====
    # 1. Список всех статей
    path('book/create/', views.BooksCreate.as_view(), name='book_create'),

    # 2. СОЗДАНИЕ (должно быть ПЕРВЫМ среди article/)
    path('book/<slug:slug>/', views.BookDetail.as_view(), name='book_detail'),
    # Даёт дополнительный доступ к статье по её числовому ID.
    path('book/id/<int:pk>/', views.BookDetail.as_view(), name='book_detail_by_id'),

    # 3. Просмотр одной статьи
    path('book/<slug:slug>/update/', views.BookUpdate.as_view(), name='book_update'),

    # 4. Редактирование
    path('book/<slug:slug>/delete/', views.BookDelete.as_view(), name='book_delete'),

    # Ищет опубликованные статьи по заголовку или содержимому.
    path('search/', views.search_books, name='search'),
]

# ===== МЕДИА-ФАЙЛЫ В РЕЖИМЕ РАЗРАБОТКИ =====
if settings.DEBUG:
    # Раздаёт загруженные пользователями файлы через Django только при разработке.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
