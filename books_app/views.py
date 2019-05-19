import requests
import logging
import sys
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import Http404
from .models import Book, Author, Category
from .forms import AddBookForm, ImportBooksForm
from django.views.generic.list import ListView
from rest_framework import viewsets
from .serializer import BookSerializer
from django.contrib import messages


logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)


class BooksListView(ListView):
    """
    Create list of all books from database in alphabetical order.
    Books List beside of titles contains book's author(s), category(ies)
     and description.It allows to filter results by category and/or author.

    """
    model = Book
    paginate_by = 10
    context_object_name = 'books_list'
    template_name = 'books_app/books_list.html'

    def get(self, request, *args, **kwargs):
        author = request.GET.get('author_contains')

        category = request.GET.get('category_contains')

        if author:
            self.queryset = Book.objects.filter(
                author__name__icontains=author)

            if category:
                self.queryset = self.queryset.filter(
                    category__category_name=category)
        else:
            if category:
                self.queryset = Book.objects.filter(
                    category__category_name=category)
            else:
                self.queryset = Book.objects.prefetch_related('author')

        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                    self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_(
                    "Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        context['categories'] = Category.objects.all()

        return self.render_to_response(context)


class AddBook(View):
    """
    Add new book. If book's author already exist it will take it
    from the data base if not it willadd new author into data base.
    The same with the category.
    :return Book instance

    """
    def get(self, request):
        form = AddBookForm()
        return render(request, 'books_app/add_book.html', {'form': form})

    def post(self, request):

        form = AddBookForm(request.POST)

        if form.is_valid():

            title = form.cleaned_data.get('title').title()
            authors = form.cleaned_data.get('author')
            categories = form.cleaned_data.get('category')
            description = form.cleaned_data.get('description')

            new_book = Book.objects.create(title=title, description=description)

            authors = authors.split(', ') or authors.split(',')
            categories = categories.split(', ') or categories.split(',')

            for author in authors:
                author = author.title()
                author_object = Author.objects.get_or_create(name=author)[0]
                author_object.save()
                new_book.author.add(author_object)

            for category in categories:
                category.title()
                category_object = Category.objects.get_or_create(
                    category_name=category)[0]
                category_object.save()
                new_book.category.add(category_object)
            new_book.save()
            logger.debug(f"created '{new_book}' - new Book object with values \
                          as: title: {title}, \
                          author: {author}, category: {category},\
                         description: {description}")
            messages.success(request, 'New book has been added')

        return redirect('books_list')


class BooksViewSet(viewsets.ModelViewSet):
    """
    API that allows books to be viewed or edited.

    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ImportBookView(View):
    """
    Import new books from google API
    and save it in to the Books' Collection data base.

    """
    template_name = 'books_app/import_books.html'

    def get(self, request):
        form = ImportBooksForm()
        return render(request, 'books_app/import_books.html', {'form': form})

    def post(self, request):

        form = ImportBooksForm(request.POST)

        if form.is_valid():
            query = request.POST['query']
            try:
                r = requests.get(
                    f'https://www.googleapis.com/books/v1/volumes?q={query}')

                if r.status_code == 200:
                    result = r.json()

                    for item in result['items']:
                        # Check if book's title is already in database
                        if Book.objects.filter(
                                title=item['volumeInfo']['title']):
                            messages.warning(
                                request, f"Books with '{query}'\
                                 key have been already imported")
                            return render(request,
                                          'books_app/import_books.html',
                                          {'form': form})
                        else:
                            # Create Book's object with suitable fields
                            # imported from google API
                            if 'authors' in item['volumeInfo']:
                                book = Book()
                                book.title = item['volumeInfo']['title']
                                if 'description' in item['volumeInfo']:
                                    book.description = item['volumeInfo']['description']
                                book.save()
                                for author in item['volumeInfo']['authors']:

                                    aut = Author.objects.get_or_create(
                                        name=author)[0]
                                    book.author.add(aut)

                                if 'categories' in item['volumeInfo']:
                                    for category in item['volumeInfo']['categories']:

                                        cat = Category.objects.get_or_create(
                                            category_name=category)[0]
                                        book.category.add(cat)

                    messages.success(request,
                                     'New books have been imported from API')
                    return redirect('books_list')
            except ConnectionError as e:
                    print(e, file=sys.stderr)
                    messages.warning(request, 'Could not connect to the API')
                    print('Could not connect to the API.')
                    exit()
                    messages.warning(request, 'Could not connect to the API')

                    return render(request,
                                  'books_app/import_books.html',
                                  {'form': form })