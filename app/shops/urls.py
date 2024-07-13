from django.urls import path

from . import views

app_name = "shops"
urlpatterns = [
    path("<int:id>/<slug:slug>/", views.product_detail, name="product_detail"),
    path("<slug:category_slug>/", views.product_list, name="product_list_by_category"),
    path("", views.product_list, name="product_list"),
]
