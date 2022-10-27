from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from todoapp import forms
from todoapp.models import Todos
from django.contrib import messages
from todoapp.decorators import signin_required
from django.utils.decorators import method_decorator
# Create your views here.
class SignUpView(CreateView):
    template_name = "registration.html"
    form_class = forms.RegistrationForm
    model = User
    success_url = reverse_lazy("signin")
    def form_valid(self, form):
        messages.success(self.request,"account has been created")
        return super().form_valid(form)
    # def get(self,request,*args,**kwargs):
    #     form=forms.RegistrationForm()
    #     return render(request,"registration.html",{"form":form})
    #
    # def post(self,request,*args,**kwargs):
    #     form=forms.RegistrationForm(request.POST)
    #     if form.is_valid():
    #         User.objects.create_user(**form.cleaned_data)
    #         messages.success(request,"registration successfull!!")
    #         return redirect("signin")
    #     else:
    #         messages.error(request,"registration failed!!")
    #         return render(request,"registration.html",{"form":form})

class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=forms.LoginForm()
        return render(request,"login.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=forms.LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pwd)
            if user:
                login(request,user)
                print("login success")
                return redirect("index")
            else:
                messages.error(request,"invalid username or password")
                print("invalid credentials")
                return render(request,"login.html",{"form":form})
        return render(request,"login.html")

@method_decorator(signin_required,name="dispatch")
class IndexView(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["Todos"]=Todos.objects.filter(user=self.request.user,status=False)
        return context
    # def get(self,request,*args,**kwargs):
    #     return render(request,"home.html")

@method_decorator(signin_required,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

@method_decorator(signin_required,name="dispatch")
class ToDoAddView(CreateView):
    template_name = "add-todo.html"
    form_class = forms.ToDoForm
    model = Todos
    success_url = reverse_lazy("list-todo")
    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"todo created")
        return super().form_valid(form)

    # def get(self,request,*args,**kwargs):
    #        form=forms.ToDoForm()
    #        return render(request,"add-todo.html",{"form":form})
    #
    # def post(self,request,*args,**kwargs):
    #     form=forms.ToDoForm(request.POST)
    #     if form.is_valid():
    #         form.instance.user=request.user
    #         form.save()
    #         messages.success(request,"todo has been added")
    #         return redirect("index")
    #     else:
    #         messages.error(request,"failed!!")
    #         return render(request,"add-todo.html",{"form":form})

@method_decorator(signin_required,name="dispatch")
class ToDoListView(ListView):
    template_name = "list-todo.html"
    context_object_name = "todos"
    model = Todos
    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)
    # def get(self,request,*args,**kwargs):
    #     all_todos=Todos.objects.filter(user=request.user)
    #     return render(request,"list-todo.html",{"todos":all_todos})


@signin_required
def delete_todo(request,*args,**kwargs):
    id=kwargs.get("id")
    Todos.objects.get(id=id).delete()
    return redirect("list-todo")

@method_decorator(signin_required,name="dispatch")
class ToDoDetailView(DetailView):
    template_name = "todo-detail.html"
    model = Todos
    context_object_name = "todo"
    pk_url_kwarg = "id"

    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("id")
    #     todo=Todos.objects.get(id=id)
    #     return render(request,"todo-detail.html",{"todo":todo})

@method_decorator(signin_required,name="dispatch")
class ToDoEditView(UpdateView):
    model=Todos
    form_class = forms.ToDoChangeForm
    template_name = "todo-edit.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("list-todo")
    def form_valid(self, form):
        messages.success(self.request,"todo has been updated")
        return super().form_valid(form)


    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("id")
    #     todo=Todos.objects.get(id=id)
    #     form=forms.ToDoChangeForm(instance=todo)
    #     return render(request,"todo-edit.html",{"form":form})

    # def post(self,request,*args,**kwargs):
    #     id=kwargs.get("id")
    #     todo=Todos.objects.get(id=id)
    #     form=forms.ToDoChangeForm(request.POST,instance=todo)
    #     if form.is_valid():
    #         msg="todo has been updated"
    #         messages.success(request,msg)
    #         form.save()
    #         return redirect("list-todo")
    #     else:
    #         msg="todo updation failed"
    #         messages.error(request,msg)
    #         return render(request,"todo-edit.html",{"form":form})
        
