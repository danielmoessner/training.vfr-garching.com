from django.urls import path
from . import views

urlpatterns = [
    # auth stuff
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # view stuff
    path('', views.TrainingListView.as_view(), name='training_list'),
    path('training/<int:pk>/', views.TrainingDetailView.as_view(), name='training_detail'),
    path('favoriten/', views.BookmarksView.as_view(), name='training_bookmarks'),
    path('generator/', views.GeneratorView.as_view(), name='generator'),
    # form stuff
    path('suche/', views.SearchFormView.as_view(), name='search'),
    path('altersgruppe-speichern/', views.AgeGroupFormView.as_view(), name='save_age_group'),
    path('schwierigkeiten-speichern/', views.DifficultiesFormView.as_view(), name='save_difficulties'),
    # save stuff on get
    path('suche-zuruecksetzen/', views.ResetSearchView.as_view(), name='reset_search'),
    path('training/<int:pk>/lesezeichen/', views.BookmarkTrainingView.as_view(), name='training_bookmark'),
    path('altersgruppe-zuruecksetzen/', views.ResetAgeGroupView.as_view(), name='reset_age_group'),
    path('filter-zuruecksetzen/', views.ResetTrainingFiltersView.as_view(), name='reset_training_filters'),
    path('schwierigkeit-zuruecksetzen', views.ResetDifficultyView.as_view(), name='reset_difficulty'),
    # api stuff
    path('api/filter_groups/<int:pk>/', views.ToggleFilterGroupApiView.as_view(), name='api_toggle_filter_group'),
    path('api/training_filters/<int:pk>/', views.ToggleTrainingFilterApiView.as_view(),
         name='api_toggle_training_filter'),
]
