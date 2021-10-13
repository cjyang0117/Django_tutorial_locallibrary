from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
# from django.shortcuts import get_object_or_404

# Create your views here.
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    # However, as you get into the tens or hundreds of records the page will take 
    # progressively longer to load (and have far too much content to browse sensibly). 
    # The solution to this problem is to add pagination to your list views, reducing 
    # the number of items displayed on each page. 
    # With this addition, as soon as you have more than 10 records the view will start 
    # paginating the data it sends to the template. The different pages are accessed using 
    # GET parameters — to access page 2 you would use the URL /catalog/books/?page=2.
    paginate_by = 2
    # context_object_name = 'my_book_list'   # your own name for the list as a template variable, defalt: catalog/book_list.html

    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war


# If a requested record does not exist then the generic class-based detail view
# will raise an Http404 exception for you automatically — in production, this 
# will automatically display an appropriate "resource not found" page, which you can customise if desired.
class BookDetailView(generic.DetailView):
    # defalt: catalog/book_detail.html
    model = Book


# The code fragment below demonstrates how you would implement the class-based view 
# as a function if you were not using the generic class-based detail view.
# def book_detail_view(request, primary_key):
#     try:
#         book = Book.objects.get(pk=primary_key)
#     except Book.DoesNotExist:
#         raise Http404('Book does not exist')

#     return render(request, 'catalog/book_detail.html', context={'book': book})


# Alternatively, we can use the get_object_or_404() function as a shortcut to 
# raise an Http404 exception if the record is not found.
# def book_detail_view(request, primary_key):
#     book = get_object_or_404(Book, pk=primary_key)
#     return render(request, 'catalog/book_detail.html', context={'book': book})


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetail(generic.DetailView):
    model = Author