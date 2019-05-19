from django.db import models

# Create your models here.


class Author(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.category_name


class Book(models.Model):

    title = models.CharField(max_length=150)
    author = models.ManyToManyField(Author)
    category = models.ManyToManyField(Category)
    description = models.TextField(max_length=500)

    def get_authors(self):
        """
        Create list from all authors

        """
        authors_list = []
        for aut in self.author.all():
            authors_list.append(aut)

        return authors_list

    def get_categories(self):
        """
        Create list from all categories

        """
        categories_list = []
        for cat in self.category.all():
            categories_list.append(cat)

        return categories_list

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
