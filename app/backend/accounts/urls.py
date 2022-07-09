from django.urls import path

from . import views

urlpatterns = [
    path('signup', views.SignUpView.as_view()),
    path('login', views.LogInView.as_view(), name='login'),
    path('naver/login/<str:code>/<str:state>', views.NaverLoginView.as_view()),
    path('kakao/login/<str:code>', views.KakaoLoginView.as_view()),
    path('userInfo/<int:user_id>', views.BeginningUserInfoView.as_view()),
    path('dayInfo/<str:date>/<int:user_id>', views.DayUserInfoView.as_view()),
]