from django.shortcuts import render
from django.http import HttpResponse
from .models import Todo
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from .todo_components import TodoList

# Http Views
@csrf_protect
def todo_list(request):
    todos = Todo.objects.all().order_by("-created_at")
    return render(request, "todo_app/todo_list.html", {"todos_list": TodoList(todos)})

@require_http_methods(["POST"])
@csrf_protect
def create_todo(request):
    title = request.POST.get("title")
    if title:
        Todo.objects.create(title=title)
    # For HTMX, we'll return the updated list
    todos = Todo.objects.all().order_by("-created_at")
    return HttpResponse(TodoList(todos))
