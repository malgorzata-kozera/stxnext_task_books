import pytest
from django.test import TestCase
from books_app.models import Book, Category, Author
from books_app.forms import AddBookForm


class TestTasks(TestCase):
    def setUp(self):
        author = Author.objects.get_or_create(name='test author')[0]
        self.author = author
        category = Category.objects.get_or_create(
            category_name='test category')[0]
        self.category = category
        book = Book.objects.create(title='test book',
                                   description='test description')
        book.author.add(self.author)
        book.category.add(self.category)
        self.book = book

    def test_save_book_with_one_author_one_category_properly(self):
        """
        Test that books are saved on database properly
        """
        books = Book.objects.all()
        assert len(books) == 1
        book = books[0]
        assert book == self.book

    def test_save_book_with_multiple_authors_properly(self):
        """
        Test that books are saved on database properly when they have more
        then one author
        """
        authors = ['test_author3', 'test author2']
        for author in authors:
            test_aut = Author.objects.get_or_create(name=author)[0]
            self.book.author.add(test_aut)
        books = Book.objects.all()
        assert len(books) == 1
        book = books[0]
        assert book == self.book

    def test_save_book_with_multiple_categories_properly(self):
        """
        Test that books are saved on database properly when they have more
        then one category
        """
        categories = ['test category1', 'test category2', 'test category']
        for category in categories:
            test_cat = Category.objects.get_or_create(
                category_name=category)[0]
            self.book.category.add(test_cat)
        books = Book.objects.all()
        assert len(books) == 1
        book = books[0]
        assert book == self.book

    def test_books_listed_for_selected_author(self):
        """Test that books are listed only for selected author"""

        assert len(Book.objects.filter(author=self.author)) == 1

    def test_books_listed_for_selected_category(self):
        """Test that books are listed only for selected category"""

        assert len(Book.objects.filter(category=self.category)) == 1

    def test_tasks_form_validation(self):
        """Test that data form is valid, form field can not be empty"""
        form_data = {'title': 'test tile', 'author': 'test author',
                     'category': 'test category',
                     'description': 'test description'}
        form = AddBookForm(data=form_data)
        assert form.is_valid() is True
