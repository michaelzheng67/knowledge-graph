from django.urls import path

from . import views

app_name = "kgraph"
urlpatterns = [
    path("", views.CategoryView, name="categories"),
    path("<int:pk>", views.InfoView.as_view(), name="info"),
    path("create_category", views.CreateCategoryView, name="create_category"),
    path("get_help", views.GetHelpView.as_view(), name="get_help"),
    path("create_new_category", views.create_new_category, name="create_new_category"),
    path("delete_category/<int:category_id>", views.delete_category, name="delete_category"),

    path("create_info/<int:category_id>", views.CreateInfoView, name="create_info"),
    path("create_new_info/<int:category_id>", views.create_new_info, name="create_new_info"),
    path("delete_info/<int:category_id>/<int:info_id>", views.delete_info, name="delete_info"),

    path("quiz_me/<int:category_id>", views.quiz_me, name="quiz_me"),
    path("increment_category/<int:category_id>", views.increment_category, name="increment_category"),
]