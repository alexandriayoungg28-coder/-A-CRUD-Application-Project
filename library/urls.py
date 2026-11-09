from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("books/", views.book_list, name="book_list"),
    path("books/<int:book_id>/", views.book_detail, name="book_detail"),
    path("books/new/", views.book_create, name="book_create"),
    path("books/<int:book_id>/edit/", views.book_update, name="book_update"),
    path("books/<int:book_id>/delete/", views.book_delete, name="book_delete"),
    path("reviews/new/", views.review_create, name="review_create"),
    path("reviews/<int:review_id>/edit/", views.review_update, name="review_update"),
    path("reviews/<int:review_id>/delete/", views.review_delete, name="review_delete"),
]