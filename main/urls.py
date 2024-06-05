from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('index/', views.index),
    path('course/', views.allCourses, name='allCourses'),
    path('course/<int:idd>/', views.getCourse, name='getCourse'),
    path('course/add/', views.createCourse, name='createCourse'),
    path('course/delete/<int:idd>', views.deleteCourse, name='deleteCourse'),
    path('course/edit/<int:idd>', views.editCourse, name='editCourse'),
    path('course/add/comment/<int:idd>', views.CreateComment.as_view(), name='addComment'),
    path('course/edit/comment/<int:idd>', views.UpdateComment.as_view(), name='editComment'),
    path('course/comment/delete/<int:idd>', views.deleteComment, name='deleteComment'),
    path('course/order/<str:name>', views.SortCourses.as_view(), name='order'),
    path('course/search/param', views.SortForm.as_view(), name='search'),
    path('course/search', views.SearchForm.as_view(), name='searchOrder'),
    path('login/', views.logs, name='my_logins'),
    path('logout/', views.logout_my, name='my_logouts'),
    path('register/', views.RegisterForm.as_view(), name='register'),
    path('login/change/password', views.PasswordChange.as_view(), name='changePassword'),
    path('login/change/password/done', PasswordChangeDoneView.as_view(template_name="done.html"),
         name='changePasswordDone'),
    path('user/', views.DetailUser.as_view(), name='detailUser'),
    path('user/update/', views.UpdateUser.as_view(), name='updateUsr'),
    path('course/buy/<int:idd>', views.buy_any_course, name='buyCourse'),
    path('user/role/', views.choose_group, name='userRole'),
    path('user/admin/', views.AdminView.as_view(), name='admin_all'),
    path('user/admin/edit/<int:idd>', views.UpdateUser_Admin.as_view(), name='editAdmin'),
    path('profile/', TemplateView.as_view(template_name="profile.html"), name='profile'),
    path('hello/', views.tasks, name='tasks'),
]
