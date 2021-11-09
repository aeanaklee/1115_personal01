"""interview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import blog.views
import account.views as account

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', blog.views.home, name="home"),
    path('blog/all_list', blog.views.all_list, name="all_list"),
    path("blog/<int:blog_id>", blog.views.detail, name="detail"),
    path('blog/new', blog.views.new, name="new"),
    path('blog/create', blog.views.create, name="create"),
    path('blog/edit/<int:blog_id>', blog.views.edit, name="edit"),
    path('blog/update/<int:blog_id>', blog.views.update, name="update"),
    path('blog/delete/<int:blog_id>', blog.views.delete, name="delete"),
    path('blog/<int:blog_id>/comment',
         blog.views.add_comment_to_post, name="add_comment_to_post"),

    path('account/login', account.login_view, name="login"),
    path('account/logout', account.logout_view, name="logout"),
    path('account/register', account.register_view, name="register"),

    path('delete_comment/<int:blog_id>/<int:comment_id>',
         blog.views.delete_comment, name="delete_comment"),
    path('blog/edit_comment/<int:blog_id>/<int:comment_id>',
         blog.views.edit_comment, name="edit_comment"),
    path('blog/update_comment/<int:comment_id>',
         blog.views.update_comment, name="update_comment"),

    path('blog/cate01', blog.views.cate01, name="cate01"),
    path('blog/cate02', blog.views.cate02, name="cate02"),
    path('blog/search', blog.views.search, name="search"),
    path('blog/search01', blog.views.search01, name="search01"),
    path('blog/search02', blog.views.search02, name="search02"),

    path('blog/mypage', blog.views.mypage, name="mypage"),
    path('blog/like', blog.views.likes, name="likes"),
    path('account/edit_user', account.edit_user, name="edit_user"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
