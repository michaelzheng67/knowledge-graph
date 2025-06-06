from django.urls import path

from . import views

app_name = "kgraph"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("categories", views.CategoryView, name="categories"),
    path("categories/<int:pk>", views.InfoView.as_view(), name="info"),
    path("categories/create_category", views.CreateCategoryView, name="create_category"),
    path("categories/create_new_category", views.create_new_category, name="create_new_category"),
    path("categories/delete_category/<int:category_id>", views.delete_category, name="delete_category"),

    path("categories/create_info/<int:category_id>", views.CreateInfoView, name="create_info"),
    path("categories/create_new_info/<int:category_id>", views.create_new_info, name="create_new_info"),
    path("categories/delete_info/<int:category_id>/<int:info_id>", views.delete_info, name="delete_info"),

    path("categories/quiz_me/<int:category_id>", views.quiz_me, name="quiz_me"),
    path("categories/increment_category/<int:category_id>", views.increment_category, name="increment_category"),


    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]