from django.urls import path
from . import views

urlpatterns = [
    # auth stuff
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # view stuff
    path('', views.TrainingListView.as_view(), name='training_list'),
    path('training/<int:pk>/', views.TrainingDetailView.as_view(), name='training_detail'),
    # reset stuff
    path('altersgruppe-zuruecksetzen/', views.ResetAgeGroupView.as_view(), name='reset_age_group'),
    path('filter-zuruecksetzen/', views.ResetTrainingFiltersView.as_view(), name='reset_training_filters'),
    # api stuff
    path('api/filter_groups/<int:pk>/', views.ToggleFilterGroupApiView.as_view(), name='api_toggle_filter_group'),
    path('api/training_filters/<int:pk>/', views.ToggleTrainingFilterApiView.as_view(),
         name='api_toggle_training_filter'),
]
