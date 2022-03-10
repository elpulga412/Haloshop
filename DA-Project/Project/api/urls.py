from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("orders", views.OrderViewSet)
router.register("products", views.ProductViewSet)
router.register("variations", views.VariationViewSet)
router.register("versions", views.VersionViewSet)
router.register("series", views.SeriesViewSet)
router.register("category", views.CategoryViewSet)
router.register("customer", views.CustomerViewSet)
router.register("reviews", views.ReviewViewSet)
router.register("news", views.NewsViewSet)
# /orders/ - GET
# /orders/ - POST
# /orders/{course_id}/ - GET
# /orders/{course_id}/ - PUT
# /orders/{course_id}/ - DELETE

urlpatterns = [
    path('', include(router.urls)),
    # path("product-list/", views.product_list, name="product_list"),
    # path("product-update/<str:pk>/", views.product_update, name="product_update"),
    # path("variation-list/", views.variation_list, name="variation_list"),
    # path("variation-update/<str:pk>/", views.variation_update, name="variation_update"),
    # path("series-list/", views.series_list, name="series_list"),
]
