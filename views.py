from django.shortcuts import render, redirect, get_object_or_404
from .models import user
from .forms import UserForm  # Create a form to simplify CRUD operations

# CREATE
def create_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = UserForm()
    return render(request, 'myapp/book_form.html', {'form': form})

# READ
def list_users(request):
    User = user.objects.all()
    return render(request, 'myapp/book_list.html', {'user': User})

# UPDATE
def update_user(request, pk):
    User = get_object_or_404(user, pk=pk)
    if request.method == "POST":
        form = UserForm(request.POST, instance=User)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = UserForm(instance=User)
    return render(request, 'myapp/book_form.html', {'form': form})

# DELETE
def delete_user(request, pk):
    User = get_object_or_404(user, pk=pk)
    if request.method == "POST":
        User.delete()
        return redirect('list_books')
    return render(request, 'myapp/book_confirm_delete.html', {'User': User})
