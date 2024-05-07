from django.shortcuts import render,redirect
from todo.models import Todo
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="/login/")
def create_todo(request):
    if request.method =="POST":
        data = request.POST
        todo_title = data.get("todo_title")
        todo_description = data.get("todo_description")
        
        todo = Todo(
            todo_title=todo_title,
            todo_description=todo_description,
            user = request.user
        )
        todo.save()
        
        messages.info(request,"Todo Created Successfully")
        return redirect("/all-todo/")
    
    return render(request, "create_todo.html")


# create a method for getting all todos
@login_required(login_url="/login/")
def all_todo(request):
    todos = Todo.objects.filter(user = request.user).filter(is_completed=False)
    
    if request.GET.get("search"):
        todos = todos.filter(todo_title__icontains=request.GET.get("search"))
    # print(todos)
    return render(request, "all_todo.html", context={"todos":todos})


# creating a method for update todo
@login_required(login_url="/login/")
def update_todo(request, id):

    # get perticular todo from db
    todo = Todo.objects.get(id=id)
    
    # check if todo is exist or not
    if not todo:
        messages.info(request,"Todo Not Found") 
        return
    
    if request.method=="POST":
        todo.todo_title = request.POST.get("todo_title")
        todo.todo_description = request.POST.get("todo_description")
        
        todo.save()
        messages.info(request,"Update Successfully")        
        return redirect('/all-todo/')
    
    return render(request, "update_todo.html", context={"todo": todo})



# render complete todo page
@login_required(login_url="/login/")
def complete_todo(request):
    todos = Todo.objects.filter(user = request.user).filter(is_completed=True)
    
    if request.GET.get("search"):
        todos = todos.filter(todo_title__icontains=request.GET.get("search"))
        
    return render(request, "complete_todo.html", context={"todos":todos})

# mark as completed
@login_required(login_url="/login/")
def mark_as_complete(request,id):
     # get perticular todo from db
    todo = Todo.objects.get(id=id)
    
    # check if todo is exist or not
    if not todo:
        messages.info(request,"Todo Not Found") 
        return
    
    todo.is_completed = True
    todo.save()
    return redirect("/all-todo/")
    



# delete todo
@login_required(login_url="/login/")
def delete_todo(request,id):
    todo = Todo.objects.get(id=id)
    
     # check if todo is exist or not
    if not todo:
        messages.info(request,"Todo Not Found") 
    
    todo.delete()
    return redirect("/all-todo/")
        



# creating user registration method 
def user_register(request):
    
    if request.user.is_authenticated:
        return redirect("/")
    
    # check the method is post or not
    if request.method=="POST":
        
        # getting data from form
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # get the user from the database based on username
        user = User.objects.filter(username = username)

        # if user is exist, show an error message
        if user.exists():
            messages.info(request, "Username Already Taken")
            return redirect("/register/")
        
        # if user is not exist, then create a user object
        user = User(
            first_name = first_name,
            last_name = last_name,
            username = username,
        )
        # using set_password method to convert the user given password to non-understandable password
        user.set_password(password)
        # save the user model
        user.save()
        
        # send a message
        messages.info(request,"Account Created Successfully")
        # return the response
        return redirect("/login/")
    
    return render(request, "register.html")



# creating a user login method
def user_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    # check the method is post or not
    if request.method == "POST":
        
        # getting data from form
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        
        # get user from database based on username
        user = User.objects.filter(username=username)

        # check user exists or not
        # if not exist
        if not user.exists():
            messages.error(request, "Invalid Username")
            return redirect("/login/")
        
        # if exist
        user = authenticate(username = username, password=password)

        # check user is given correct password or not
        if user is None:
            messages.info(request, "Incorrect Password")
            return redirect("/login/")
        else:
            login(request, user)
            return redirect("/all-todo/")
    
    return render(request, "login.html")



# user logout method
def user_logout(request):
    logout(request)
    return redirect("/login/")