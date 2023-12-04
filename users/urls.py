from django.urls import path
from users.views import SignUpView, LoginView, RankingView, RankingDB, Ranking_all_View

urlpatterns = [
    path('signup', SignUpView.as_view()),
    path('login', LoginView.as_view()),
    path('ranking', RankingView.as_view()),
    path('rankingDB', RankingDB.as_view()),
    path('ranking_all', Ranking_all_View.as_view()),

]