from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordChangeView
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, ListView, DetailView, UpdateView

from tasq.tasks import big_data
from main.forms import CourseForm, CommentForm, SortingForm, LoginForm, UserForm, UserProfileForm, ChooseGroupForm, \
    FullUpdateOfUserForm
from main.models import Course, Comment, User


# Create your views here.
def index(request):
    return render(request, 'hi.html')


def getRole(role, user):
    return user.groups.all().filter(name__in=role).exists()


# @cache_page(60 * 1)
def allCourses(request):
    cats = cache.get('allCourses')
    if cats is None:
        cats = Course.objects.all()
        cache.set('allCourses', cats, 30)
    # courses = Course.objects.all()
    context = {'courses': cats, "name": 'name', "price": 'price'}
    return render(request, "all.html", context)


@login_required(login_url="my_logins")
def getCourse(request, idd):
    course = Course.objects.get(pk=idd)
    context = {'course': course}
    print(request.user)
    return render(request, 'get.html', context)


@login_required(login_url="my_logins")
def createCourse(request):
    if not getRole(['TEACHER'], request.user):
        raise PermissionDenied
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            c = form.save(commit=False)
            c.owner_user_id = request.user.id
            c.save()
            print("Hello world")
            return redirect("allCourses")
    else:
        form = CourseForm()
    return render(request, "create.html", {"form": form})


def editCourse(request, idd):
    course = Course.objects.get(pk=idd)
    if not ((getRole(['TEACHER'], request.user) and course.owner_user_id == request.user.id) or getRole(['ADMIN'],
                                                                                                        request.user)):
        raise PermissionDenied
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            course.name = cd['name']
            course.description = cd['description']
            course.creator = cd['creator']
            course.price = cd['price']
            course.image = cd['image']
            course.save()
            return redirect("allCourses")
    else:
        form = CourseForm()
        form.fields['name'].initial = course.name
        form.fields['description'].initial = course.description
        form.fields['creator'].initial = course.creator
        form.fields['price'].initial = course.price
    return render(request, "update.html", {"form": form})


def deleteCourse(request, idd):
    course = Course.objects.get(pk=idd)
    if not ((getRole(['TEACHER'], request.user) and course.owner_user_id == request.user.id) or getRole(['ADMIN'],
                                                                                                        request.user)):
        raise PermissionDenied
    course.delete()
    return redirect("allCourses")


class CreateComment(FormView):
    form_class = CommentForm
    template_name = "createComment.html"
    success_url = reverse_lazy("allCourses")
    pk_url_kwarg = "idd"

    def form_valid(self, form):
        p = self.kwargs['idd']
        s = form.save(commit=False)
        s.course_id = p
        s.save()
        return super().form_valid(form)


class UpdateComment(FormView):
    form_class = CommentForm
    template_name = "updateComment.html"
    success_url = reverse_lazy("allCourses")
    pk_url_kwarg = "idd"

    def form_valid(self, form):
        c = Comment.objects.get(pk=self.kwargs['idd'])
        c.text = form.cleaned_data['text']
        c.save()
        return super().form_valid(form)


def deleteComment(request, idd):
    comment = Comment.objects.get(pk=idd)
    comment.delete()
    return redirect("allCourses")


class SortCourses(ListView):
    model = Course
    context_object_name = 'cor'
    template_name = "sort.html"
    name_url_kwarg = "name"

    def get_queryset(self):
        return Course.objects.all().order_by(self.kwargs["name"])


class SortForm(FormView):
    form_class = SortingForm
    template_name = 'foo.html'
    success_url = reverse_lazy("searchOrder")

    def form_valid(self, form):
        response = HttpResponse('settings cookie')
        response.set_cookie('color', 'blue', max_age=180)
        print(form.cleaned_data['choice1'])
        ch = []
        for i in form.cleaned_data['choice1']:
            ch.append(i.pk)
        self.request.session['choice1'] = ch
        self.request.session['price'] = form.cleaned_data['price']
        self.request.session['choice'] = form.cleaned_data['choice']
        self.request.session['which'] = form.cleaned_data['which']
        return super().form_valid(form)


class SearchForm(ListView):
    model = Course
    context_object_name = 'cor'
    template_name = 'view.html'

    def get_queryset(self):
        if self.request.COOKIES.get('color'):
            print(self.request.COOKIES.get('color'))
        else:
            print("cookie has not found")
        print(self.request.session['choice'])
        print(self.request.session['choice1'])
        print(self.request.session['price'])
        if self.request.session['which'] == 1:
            return Course.objects.filter(id__in=self.request.session['choice1'])
        else:
            if self.request.session['choice'] == 'lt':
                return Course.objects.filter(price__lt=self.request.session['price'])
            elif self.request.session['choice'] == 'gt':
                return Course.objects.filter(price__gt=self.request.session['price'])
            elif self.request.session['choice'] == 'eq':
                return Course.objects.filter(price=self.request.session['price'])
        return Course.objects.all()


# start authentication code
def logs(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            u = authenticate(request, username=username, password=password)
            if u is not None and u.is_active:
                login(request, u)
                return redirect("allCourses")
            else:
                return HttpResponse("Invalid login or password")
        else:
            return render(request, 'log.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'log.html', {'form': form})


def logout_my(request):
    logout(request)
    return HttpResponse('logout success')


class RegisterForm(FormView):
    form_class = UserForm
    template_name = "reg.html"
    success_url = reverse_lazy("my_logins")

    def form_valid(self, form):
        u = form.save(commit=False)
        u.set_password(form.cleaned_data['password'])
        u.save()
        return super().form_valid(form)


class PasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "pass.html"
    success_url = reverse_lazy("changePasswordDone")


# end authentication code


class DetailUser(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "usr.html"
    context_object_name = "usr"
    login_url = reverse_lazy("my_logins")
    extra_context = {
        "is_admin": False,
    }

    def get_object(self, queryset=None):
        return get_user_model().objects.get(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = False
        context['role'] = 'None'
        if self.request.user.groups.all().exists():
            context['role'] = self.request.user.groups.all()[0].name
        if self.request.user.groups.all().filter(name="ADMIN").exists():
            context["is_admin"] = True
            print("ADMIN GROUP")
        else:
            print("is not admin")
        return context


class UpdateUser(LoginRequiredMixin, View):
    login_url = reverse_lazy("my_logins")

    def get(self, request, *args, **kwargs):
        form = UserProfileForm()
        idd = request.user.pk
        u = get_user_model().objects.get(pk=idd)
        print(u.username)
        form.fields['username'].initial = u.username
        form.fields['email'].initial = u.email
        form.fields['first_name'].initial = u.first_name
        form.fields['last_name'].initial = u.last_name
        return render(request, 'up.html', {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(request.POST, request.FILES)
        u = get_user_model().objects.get(pk=request.user.pk)
        if form.is_valid():
            u.username = form.cleaned_data['username']
            u.email = form.cleaned_data['email']
            u.first_name = form.cleaned_data['first_name']
            u.last_name = form.cleaned_data['last_name']
            u.balance = form.cleaned_data['balance']
            u.photo = form.cleaned_data['photo']
            u.save()
            return redirect("detailUser")
        else:
            print(form.errors)
        return redirect("detailUser")


@login_required(login_url="my_logins")
def buy_any_course(request, idd):
    if request.method == 'POST':
        if request.POST['ch']:
            u = request.user
            c = Course.objects.get(id=idd)
            sul = u.balance - c.price
            if sul < 0:
                print("lvl3 = ", sul)
                return redirect("allCourses")
            u.balance = sul
            u.save()
            c.buy_user.add(request.user)
            c.save()
        else:
            print("lvl2")
        return redirect("detailUser")
    else:
        return render(request, "buy.html")


@login_required(login_url="my_logins")
def choose_group(request):
    if request.method == 'POST':
        form = ChooseGroupForm(request.POST)
        if form.is_valid():
            choice = form.cleaned_data['sliders']
            if choice == 'Student':
                g = Group.objects.get(name='STUDENT')
                g.user_set.add(request.user)
                g.save()
            elif choice == 'Teacher':
                g = Group.objects.get(name='TEACHER')
                g.user_set.add(request.user)
                g.save()
            elif choice == 'Admin':
                g = Group.objects.get(name='ADMIN')
                g.user_set.add(request.user)
                g.save()
            return redirect("detailUser")
    else:
        form = ChooseGroupForm()
        return render(request, "gr.html", {"form": form})


class AdminView(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = "ad_usr.html"
    context_object_name = "usr"

    def get_queryset(self):
        return get_user_model().objects.exclude(groups__name='ADMIN')

    def dispatch(self, request, *args, **kwargs):
        print(User.objects.get(pk=request.user.pk).groups.all().filter(name="ADMIN").exists())
        if not request.user.groups.all().filter(name='ADMIN').exists():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class UpdateUser_Admin(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("my_logins")
    form_class = FullUpdateOfUserForm
    pk_url_kwarg = "idd"
    template_name = "ad_up.html"
    success_url = reverse_lazy('admin_all')

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.kwargs.get('idd'))

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.all().filter(name='ADMIN').exists():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


#####################################################################


def tasks(request):
    result = big_data.delay(3)
    print(result.get(timeout=3))
    return HttpResponse("Hello World")


