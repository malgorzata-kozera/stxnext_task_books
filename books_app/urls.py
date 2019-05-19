from django.urls import path
from books_app import views


urlpatterns = [

    path('books_list', views.BooksListView.as_view(), name='books_list'),
    path('add_book', views.AddBook.as_view(), name='add_book'),
    path('import_books', views.ImportBookView.as_view(), name='import_books'),

]
