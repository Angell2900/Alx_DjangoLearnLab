from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

@permission_required('bookshelf.can_view')
def book_list(request):
    # View logic here
    pass

@permission_required('bookshelf.can_create')
def book_create(request):
    # View logic here
    pass

@permission_required('bookshelf.can_edit')
def book_edit(request, pk):
    # View logic here
    pass

@permission_required('bookshelf.can_delete')
def book_delete(request, pk):
    # View logic here
    pass
