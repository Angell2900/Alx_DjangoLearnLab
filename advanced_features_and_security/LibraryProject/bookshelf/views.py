from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    # View logic here
    pass

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    # View logic here
    pass

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    # View logic here
    pass

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    # View logic here
    pass
