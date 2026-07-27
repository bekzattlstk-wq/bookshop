# App ичиндеги китеп, избранное жана башка барактардын URL маршруттарына жооп берет.
from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search_books, name='search'),
    path('books/', views.book_list, name='book_list'),
    path('favorites/', views.favorites_page, name='favorites'),
    path('book/<slug:slug>/',views.book_detail,name='book_detail'),
    path('books/create/',views.book_create,name='book_create'),
    path('book/<slug:slug>/update/', views.book_update, name='book_update'),
    path('book/<slug:slug>/delete/',views.book_delete,name='book_delete'),
]
