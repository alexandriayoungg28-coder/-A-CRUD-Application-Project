from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.contrib import messages

from .forms import BookForm, ReviewForm
from .models import Book, Review


def book_list(request):
    query = request.GET.get("q", "").strip()
    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    elif request.GET.get("search_submit"):
        messages.error(request, "Please enter a title or author to search.")

    return render(
        request,
        "library/Book-Listings.html",
        {"books": books, "query": query},
    )


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.review_set.select_related("user").all()

    return render(
        request,
        "library/book_detail.html",
        {"book": book, "reviews": reviews},
    )


def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)  # Include request.FILES for file uploads

        if form.is_valid():
            form.save()
            messages.success(request, "Book created successfully.")
            return redirect("book_list")
    else:
        form = BookForm()

    return render(
        request,
        "library/book_form.html",
        {"form": form},
    )


def book_update(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        form = BookForm( 
            request.POST, 
            request.FILES, 
            instance=book)

        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully.")
            return redirect("book_list")
    else:
        form = BookForm(instance=book)

    return render(
        request,
        "library/book_form.html",
        {"form": form, "book": book},
    )


def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        book.delete()
        messages.success(request, "Book deleted successfully.")
        return redirect("book_list")

    return render(
        request,
        "library/book_confirm_delete.html",
        {"book": book},
    )

def review_create(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Review submitted successfully.")
            return redirect("book_list")
    else:
        form = ReviewForm()

    return render(
        request,
        "library/Review-Form.html",
        {"form": form},
    )

def review_update(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            form.save()
            messages.success(request, "Review updated successfully.")
            return redirect("book_detail", book_id=review.book.id)
    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        "library/Review-Form.html",
        {"form": form, "review": review},
    )


def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.method == "POST":
        review.delete()
        messages.success(request, "Review deleted successfully.")
        return redirect("book_list")

    return render(
        request,
        "library/review_confirm_delete.html",
        {"review": review},
    )


def home(request):
    return render(request, "library/home.html")