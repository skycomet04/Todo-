from django.shortcuts import render,redirect,HttpResponse
from.models import Todo
from django.contrib import messages
from .forms import Formtodo
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.views import generic
from django.urls import reverse_lazy

def updateitem(request,tid):
    up_item=Todo.objects.get(id=tid)
    if request.user!=up_item.creator:
        return HttpResponse("User not allowed to make changes .Only user who created it can make changes!!")
    form=Formtodo(instance=up_item)       
    if request.method =='POST':
        form=Formtodo(request.POST, instance=up_item)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = Formtodo(instance=up_item)
    return render(request,'updatetask.html',{'task':form})

def index(request):
    itemlist=None
    if request.user.is_authenticated:
        itemlist=Todo.objects.filter(creator=request.user).values()
    else:
        HttpResponse("user is not authenticated")
    if request.method =='POST':
        form=Formtodo(request.POST)       
        if form.is_valid():
            todo_ins=form.save(commit=False)
            todo_ins.creator=request.user
            todo_ins.save()
            return redirect('index')
    else:
        form=Formtodo()
    context={'form':form,'item_list':itemlist}
    return render(request,'index.html',context,)

def remove(request, item_id):
    if request.user.is_authenticated:
        item = Todo.objects.get(id=item_id)
        if request.user==item.creator:
            item.delete()
            messages.info(request, "item removed !!!")
        return redirect('index')
    else:
        return redirect('log_in')
    
class Userregisterview(generic.CreateView):
    form_class=UserCreationForm
    template_name='register.html'
    success_url=reverse_lazy('log_in')

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, f'account does not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'login.html',{'form':form})
def log_out(request):
    logout(request)
    return redirect('log_in')
