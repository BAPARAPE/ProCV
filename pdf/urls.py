from django.conf.urls.static import static
from django.urls import path
from CV import settings
from pdf.views import index, formulaire, cv, login_user, signup, logout_user, update_cv, dashboard, generer_cv, supprimer_cv
urlpatterns = [
    path('', index, name="index"),
    path('formulaire', formulaire, name="formulaire"),
    path('update_cv', update_cv, name="update_cv"),
    path('supprimer_cv', supprimer_cv, name="supprimer_cv"),
    path('generer_cv', generer_cv, name="generer_cv"),
    path('dashboard', dashboard, name="dashboard"),
    path('cv', cv, name="moncv"),
    path('logout_user', logout_user, name="logout_user"),
    path('signup', signup, name="signup"),
    path('login', login_user, name="login_user"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)