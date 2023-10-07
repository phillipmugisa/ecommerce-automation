from django.urls import path
from manager import views as ManagerViews

app_name = "manager"

urlpatterns = [
    path("", ManagerViews.HomeView.as_view(), name="home"),
    path("search/", ManagerViews.ProductSearch.as_view(), name="search-product"),
    path("platform/<str:platform>/<str:product_name>/", ManagerViews.PlatformFilterView.as_view(), name="platform-filter")
]