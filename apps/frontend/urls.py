from django.urls import path
from . import views

urlpatterns = [
    # auth stuff
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # view stuff
    path('', views.ExerciseListView.as_view(), name='exercises'),
    path('uebung/<int:pk>/', views.ExerciseDetailView.as_view(), name='exercise'),
    path('favoriten/', views.BookmarksView.as_view(), name='favorites'),
    path('generator/', views.GeneratorView.as_view(), name='generator'),
    path('trainings/', views.TrainingsView.as_view(), name='trainings'),
    path('trainings/vfr/', views.TrainingsVfrView.as_view(), name='trainings_vfr'),
    path('trainings/<int:pk>/loeschen/', views.DeleteTrainingView.as_view(), name='training_delete'),
    path('trainings/<int:pk>/bearbeiten/', views.GeneratorView.as_view(), name='training_update'),
    # pdf stuff
    path('trainings/<int:pk>/', views.TrainingView.as_view(), name='training'),
    path('trainings/<int:pk>.pdf', views.TrainingPdfView.as_view(), name='training_pdf'),
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
