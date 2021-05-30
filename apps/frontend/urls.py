from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('exercises')), name='index'),
    # auth stuff
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # view stuff
    path('uebungen/', views.ExerciseListView.as_view(), name='exercises'),
    path('uebungen/<int:pk>/', views.ExerciseDetailView.as_view(), name='exercise'),
    path('uebungen/<int:pk>.pdf', views.ExercisePdfView.as_view(), name='exercise_pdf'),
    path('favoriten/', views.BookmarksView.as_view(), name='favorites'),
    path('generator/', views.GeneratorView.as_view(), name='generator'),
    path('trainings/', views.TrainingsView.as_view(), name='trainings'),
    path('trainings/vfr/', views.TrainingsVfrView.as_view(), name='trainings_vfr'),
    path('trainings/detail/', views.TrainingView.as_view(), name='training'),
    path('trainings/drucken/', views.TrainingPrintView.as_view(), name='training_print'),
    path('trainings/<int:pk>/loeschen/', views.DeleteTrainingView.as_view(), name='training_delete'),
    path('trainings/<int:pk>/bearbeiten/', views.GeneratorView.as_view(), name='training_update'),
    path('grundlagen/', views.FundamentalsView.as_view(), name='fundamentals'),
    path('einstellungen/', views.SettingsView.as_view(), name='settings'),
    # form stuff
    path('suche/', views.SearchFormView.as_view(), name='search'),
    # save stuff on get
    path('uebungen/<int:pk>/lesezeichen/', views.BookmarkTrainingView.as_view(), name='training_bookmark'),
    path('einstellungen/filter-zuruecksetzen/', views.ResetTrainingFiltersView.as_view(),
         name='reset_training_filters'),
    # api stuff
    path('api/filter_groups/<int:pk>/', views.ToggleFilterGroupApiView.as_view(), name='api_toggle_filter_group'),
    path('api/training_filters/<int:pk>/', views.ToggleTrainingFilterApiView.as_view(),
         name='api_toggle_training_filter'),
    path('api/search/', views.SearchApiView.as_view(), name='api_search')
]
