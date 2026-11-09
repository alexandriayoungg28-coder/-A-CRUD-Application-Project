
from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, default="")
    genre = models.CharField(max_length=100)
    publication_date = models.DateField()
    cover = models.ImageField(
        upload_to="book_covers/",
        blank=True,
    )
    description = models.TextField(blank=True)
    # TODO: Add a description field for the book detail page.

    def __str__(self):
        return self.title


class Review(models.Model):
    RATING_CHOICES = [
        (1, "1 - Poor"),
        (2, "2 - Fair"),
        (3, "3 - Good"),
        (4, "4 - Very Good"),
        (5, "5 - Excellent"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.CharField(max_length=200, default="")
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review of {self.book.title} by {self.user.username}"