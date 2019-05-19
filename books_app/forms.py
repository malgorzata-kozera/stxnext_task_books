from django import forms


class AddBookForm(forms.Form):

    title = forms.CharField(max_length=100)
    author = forms.CharField(max_length=100)
    category = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)


class ImportBooksForm(forms.Form):

    query = forms.CharField(label='Enter Keywords',
                            max_length=100,
                            required=False)
