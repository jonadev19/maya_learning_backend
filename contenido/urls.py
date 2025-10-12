from django.urls import path
from .views import (
    TemaListView,
    TemaDetailView,
    MaterialListView,
    MaterialDetailView,
    VocabularioListView,
    VocabularioDetailView
)

urlpatterns = [
    # Temas
    path('temas/', TemaListView.as_view(), name='tema-list'),
    path('temas/<str:id>/', TemaDetailView.as_view(), name='tema-detail'),

    # Materiales
    path('materiales/', MaterialListView.as_view(), name='material-list'),
    path('materiales/<str:id>/', MaterialDetailView.as_view(), name='material-detail'),

    # Vocabulario
    path('vocabulario/', VocabularioListView.as_view(), name='vocabulario-list'),
    path('vocabulario/<str:id>/', VocabularioDetailView.as_view(), name='vocabulario-detail'),
]
