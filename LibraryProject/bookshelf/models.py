from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    isbn = models.CharField(max_length=13)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
