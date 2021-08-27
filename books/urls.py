from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_or_register),
    path('register_user', views.register_user),
    path('login_user', views.login_user),
    path('favorite_books', views.favorite_books),
    path('add_book', views.add_book),
    path('add_fav/<int:book_id>', views.add_fav),
    path('book_page/<int:id>', views.book_page),
    path('edit_book/<int:id>', views.edit_book),
    path('delete_book/<int:id>', views.delete_book),
    path('unfavorite/<int:id>', views.unfavorite),
]