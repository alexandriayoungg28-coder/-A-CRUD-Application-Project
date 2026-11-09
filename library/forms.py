from django import forms 

from .models import Book, Review


class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["description"].required = True

    def clean_cover(self):
        cover = self.cleaned_data.get("cover")
        clear_cover = self.data.get(self.add_prefix("cover-clear"))

        if cover:
            return cover

        if self.instance.pk and self.instance.cover and clear_cover != "on":
            return self.instance.cover

        raise forms.ValidationError("Please choose a book cover.")

    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "genre",
            "publication_date",
            "cover",
            "description",
        ]
        widgets = {
            "publication_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "author": forms.TextInput(attrs={"class": "form-control"}),
            "genre": forms.TextInput(attrs={"class": "form-control"}),
            "cover": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 5}
            ),
        }
        labels = {
            "description": "Book Description",
        }


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["book"].label_from_instance = (
            lambda book: f"{book.title} - {book.author}"
        )
        self.fields["user"].empty_label = "-- Select an option --"
        self.fields["book"].empty_label = "-- Select an option --"
        self.fields["rating"].choices = [
            ("", "-- Select an option --"),
            *self.fields["rating"].choices,
        ]
        if not self.instance.pk:
            self.initial["rating"] = ""

    class Meta:
        model = Review
        fields = ["user", "book", "rating", "text"]
        widgets = {
            "user": forms.Select(attrs={"class": "form-select"}),
            "book": forms.Select(attrs={"class": "form-select"}),
            "rating": forms.Select(attrs={"class": "form-select"}),
            "text": forms.Textarea(
                attrs={"class": "form-control", "rows": 5}
            ),
        }