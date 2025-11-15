from django.urls import path, include
from Introduction_to_Django.LibraryProject.bookshelf import admin
from bookshelf import views

urlpatterns = [
    path('', views.home, name='home'),  # <-- this is the homepage
    path('admin/', admin.site.urls),
    path('books/', include('bookshelf.urls')),
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.library_detail, name='library_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
]
