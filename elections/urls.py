from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path("all_elections/", all_elections, name='all_elections'),
    path("election/<int:id>/", electionDetail, name='electionDetail'),
    path("deleteelection/<int:id>/", deleteElection, name='deleteelection'),
    # path("election/<int:id>/", electionDetail, name='electionDetail'),
    
    path("all_candidates/", all_candidates, name='all_candidates'),
    path("deletecandidate/<int:id>/", deleteCandidate, name='deletecandidate'),
    # path("election/<int:id>/", electionDetail, name='electionDetail'),
    
    path("all_results/", all_results, name='all_results'),
    path("deleteresult/<int:id>/", deleteResult, name='deleteresult'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
