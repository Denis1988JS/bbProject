from django.shortcuts import render, redirect
from  django.http import  HttpResponse, Http404
from  django.template import TemplateDoesNotExist
from  django.template.loader import get_template
from  django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AbvUser, SubRubric, Bb, Comment
from .forms import ChangeUserInfoForm, RegisterUserForm, SeachForm, BbForm, AIFormSet, UserCommentForm,GuesCommentForm
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.

#Страница о сайте
def about(request):
    return render(request, 'about.html')

#Главная страница
def index(request):
    bbs = Bb.objects.filter(is_avtive=True)[:10]
    title = 'Главная страница'
    data = {'title':title,'bbs':bbs}
    return render(request, 'index.html', context=data)

#Страница авторизация на сайте
class LoginUser(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('index')

#Страница регистрация на сайте нового пользователя
class RegisterUserView(CreateView):
    model = AbvUser
    template_name = 'register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')

#Страница пользователя
@login_required
def profile(request):
    bbs = Bb.objects.filter(autor=request.user)
    context = {'bbs':bbs}
    print(bbs)
    return render(request, 'profile.html', context)

#Выход пользователя
class LogoutPage(LoginRequiredMixin,LogoutView):
    template_name = 'logout.html'

#Страница редактирования данных пользователя
class ChangeUserInfoView(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model = AbvUser
    template_name = 'change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('profile')
    success_message = 'Данные успешно изменены'
    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset,pk=self.user_id)

#Страница редактирования пароля пользователя
class ChangePasswordUser(SuccessMessageMixin, LoginRequiredMixin,PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('profile')
    success_message = 'Пароль успешно изменен'

#Удаление пользователя
from django.views.generic.edit import DeleteView
from django.contrib.auth import logout, login
from django.contrib import messages

class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AbvUser
    template_name = 'delete_user.html'
    success_url = reverse_lazy('index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super(DeleteUserView, self).setup(request, *args,**kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS,'Пользователь удален')
        return super().setup(request, *args,**kwargs)

    def get_object(self, queryset=None):
        if not  queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

def by_rubric(request, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    bbs = Bb.objects.filter(is_avtive = True, rubric = pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__incontains = keyword) | Q(content__incontains = keyword)
        bbs = bbs.filter(q)
    else:
        keyword = ''
        form = SeachForm(initial={'keyword': keyword})
        paginator = Paginator(bbs, 2)
        if 'page' in request.GET:
            page_num = request.GET['page']
        else:
            page_num = 1
        page = paginator.get_page(page_num)
        context = {'rubric':rubric, 'page':page, 'bbs':page.object_list, 'form':form}
        return render(request, 'by_rubric.html', context)

def detail(request, rubric_pk ,pk):
    bb = get_object_or_404(Bb, pk=pk)
    ais = bb.additionalimage_set.all()
    comments = Comment.objects.filter(bb=pk, is_active = True)
    initial = {'bb': bb.pk}
    if request.user.is_authenticated:
        initial['autor'] = request.user.username
        form_class = UserCommentForm
    else:
        form_class = GuesCommentForm
    form = form_class(initial=initial)
    if request.method == "POST":
        c_form = form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.add_message(request, messages.SUCCESS, 'Комментарий добавлен')
        else:
            form = c_form
            messages.add_message(request, messages.WARNING, 'Комментарий не добавлен')

    context = {'bb': bb, 'ais':ais, 'comments':comments, 'form':form}
    return render(request, 'detail.html', context)

#Добавить объявление через пользователя
@login_required
def profile__bb_add(request):
    if request.method == "POST":
        form = BbForm(request.POST, request.FILES)
        if form.is_valid():
            bb = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=bb)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, 'Объявление добавлено')
                return redirect('profile')
    else:
        form = BbForm(initial={'autor': request.user.pk})
        formset = AIFormSet()
    context = {'form':form, 'formset':formset}
    return render(request, 'profile_bb_add.html', context)

#Поменять объявление
@login_required
def profile_bb_change(request, pk):
    bb = get_object_or_404(Bb, pk=pk)
    if request.method == 'POST':
        form = BbForm(request.POST, request.FILES, instance=bb)
        if form.is_valid():
            bb = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=bb)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, 'Объявление изменено')
                return redirect('profile')
    else:
        form = BbForm(instance=bb)
        formset = AIFormSet(instance=bb)
    context = {'form':form, 'formset':formset}
    return render(request, 'profile_bb_change.html', context)

#Удалить объявление
@login_required
def profile_bb_delete(request, pk):
    bb = get_object_or_404(Bb, pk=pk)
    bb.delete()
    messages.add_message(request, messages.SUCCESS,'Объявление удалено')
    return redirect('profile')
