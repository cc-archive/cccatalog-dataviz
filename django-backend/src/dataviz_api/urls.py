from django.urls import path
from dataviz_api import views


urlpatterns = [
    path('graph-data/', views.serve_graph_data)
]