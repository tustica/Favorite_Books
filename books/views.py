from datetime import datetime
from django.shortcuts import render, redirect
from books.models import Book, User
from django.contrib import messages
import bcrypt

def login_or_register(request):
    return render(request, 'login_and_register.html')

def register_user(request):
    errors = User.objects.validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],
        email=request.POST['email'], password=pw_hash.decode())
        messages.success(request, "Registered!")
        return redirect('/')

def favorite_books(request):
    context = {
        "user": User.objects.get(id=request.session['userid']),
        "books": Book.objects.all()
    }
    return render(request, 'favorite_books.html', context)


def login_user(request):
    # errors = User.objects.login_validator(request.POST)
    # if len(errors)>0:
    #     for key, value in errors.items():
    #         messages.error(request, value)
    #     return redirect('/')

    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
    else:
        messages.error(request, "Invalid Email")
        return redirect('/')

    if bcrypt.checkpw(request.POST['login_password'].encode(), logged_user.password.encode()):
        request.session['userid'] = logged_user.id
        return redirect('/favorite_books')
    else:
        messages.error(request, "Incorrect Password")
        return redirect('/')

def add_book(request):
    errors = Book.objects.book_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/favorite_books')
    else:
        new_book = Book.objects.create(title=request.POST['title'], description=request.POST['description'],
        uploaded_by=User.objects.get(id=request.session['userid']))
        new_book.users_who_liked.add(User.objects.get(id=request.session['userid']))
    return redirect('/favorite_books')

def add_fav(request, book_id):
    user = User.objects.get(id=request.session['userid'])
    books = Book.objects.all()
    for book in books:
        if book.id == book_id:
            book.users_who_liked.add(user)
    url = '/add_fav/'+str(book_id)
    if request.META.get('PATH_INFO') == url:
        return redirect('/book_page/'+str(book_id))
    else:
        return redirect('/favorite_books')
    
def book_page(request, id):
    user = User.objects.get(id=request.session['userid'])
    book = Book.objects.filter(id=id)
    if book:
        current_book = book[0]
    context = {
        "book": current_book,
        "user": user
    }
    return render(request, 'book_page.html', context)

def edit_book(request, id):
    errors = Book.objects.book_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/book_page/'+str(id))
    else:
        Book.objects.filter(id=id).update(description=request.POST['description'])
        Book.objects.filter(id=id).update(updated_at = datetime.now())
        return redirect('/book_page/'+str(id))

def delete_book(request, id):
    Book.objects.filter(id=id).delete()
    return redirect('/favorite_books')

def unfavorite(request, id):
    user = User.objects.get(id=request.session['userid'])
    book = Book.objects.filter(id=id)
    if book:
        current_book = book[0]
    current_book.users_who_liked.remove(user)
    return redirect('/book_page/'+str(id))