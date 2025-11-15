from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .forms import ExampleForm
from .models import Book

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            Book.objects.create(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                publication_year=form.cleaned_data['publication_year']
            )
            return render(request, 'bookshelf/form_example.html', {'form': form, 'message': 'Book created successfully'})
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    # View logic here
    pass

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    # View logic here
    pass
