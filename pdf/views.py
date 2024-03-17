from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import InfoPerso, Experience, Formation, Langue, User
from datetime import datetime
import pdfkit
from django.template.loader import get_template
import io

def index(request):
    return render(request, 'pdf/accueil.html')

# def accueil2(request):
#     return render(request, 'pdf/accueil2.html')

def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email déjà utilisé, désolé')
            return redirect('signup')
        else:
            user = User.objects.create_user(email=email, username=username, password=password)
            user.save()
            messages.success(request, 'Votre compte a été créé avec succès ! Vous pouvez maintenant vous connecter.')
            return redirect('login_user')
    else:
        return render(request, 'pdf/signup.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            infoperso = InfoPerso.objects.filter(user=user).first()
            experience = Experience.objects.filter(user=user).first()
            formation = Formation.objects.filter(user=user).first()
            if infoperso and experience and formation:
                return redirect('dashboard')
            else:
                return redirect('index')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
            return redirect('index')
    else:
        return render(request, 'pdf/login.html')

def logout_user(request):
    logout(request)
    return redirect('index')

def formulaire(request):
    if request.method == "POST":
        # Informations personnelles
        nomcv = request.POST.get("nomcv")
        prenomcv = request.POST.get("prenomcv")
        emailcv = request.POST.get("emailcv")
        numero = request.POST.get("numero")
        adresse = request.POST.get("adresse")
        profil = request.POST.get("profil")
        competence = request.POST.get("competence")
        interet = request.POST.get("interet")
        
        # Création de l'objet InfoPerso
        infoperso = InfoPerso.objects.create(
            user=request.user,
            nomcv=nomcv,
            prenomcv=prenomcv,
            emailcv=emailcv,
            numero=numero,
            adresse=adresse,
            profil=profil,
            competence=competence,
            interet=interet
        )
        
        # Expériences
        experiences = []
        for i in range(1,4):  # Boucle sur le nombre d'expériences
            poste = request.POST.get(f'poste{i}')
            societe = request.POST.get(f'societe{i}')
            adresse_exp = request.POST.get(f'adresse_exp{i}')
            date_debut = request.POST.get(f'date_debut{i}')
            date_fin = request.POST.get(f'date_fin{i}')
            description = request.POST.get(f'description{i}')
            
            # Création de l'objet Experience
            experience = Experience.objects.create(
                user=request.user,
                poste=poste,
                societe=societe,
                adresse_exp=adresse_exp,
                date_debut=date_debut,
                date_fin=date_fin,
                description=description
            )
            experiences.append(experience)
        
        # Formations
        formations = []
        for i in range(1,4):  # Boucle sur le nombre de formations
            diplome = request.POST.get(f'diplome{i}')
            etablissement = request.POST.get(f'etablissement{i}')
            adresse_formation = request.POST.get(f'adresse_formation{i}')
            date_debut_formation = request.POST.get(f'date_debut_formation{i}')
            date_fin_formation = request.POST.get(f'date_fin_formation{i}')
            
            # Création de l'objet Formation
            formation = Formation.objects.create(
                user=request.user,
                diplome=diplome,
                etablissement=etablissement,
                adresse_formation=adresse_formation,
                date_debut_formation=date_debut_formation,
                date_fin_formation=date_fin_formation
            )
            formations.append(formation)
        
        # Langues
        anglais = request.POST.get('anglais')
        francais = request.POST.get('francais')
        
        # Création de l'objet Langue
        langue = Langue.objects.create(
            user=request.user,
            anglais=anglais,
            francais=francais
        )
        
        return redirect('dashboard')
    
    return render(request, 'pdf/forms1.html')

def cv(request):
    user = request.user
    
    # Récupération des informations personnelles
    infoperso = InfoPerso.objects.get(user=user)
    nomcv = infoperso.nomcv
    prenomcv = infoperso.prenomcv
    emailcv = infoperso.emailcv
    numero = infoperso.numero
    adresse = infoperso.adresse
    profil = infoperso.profil
    competence = infoperso.competence
    interet = infoperso.interet
    
    # Récupération des expériences de l'utilisateur avec leurs détails
    experiences = []
    for experience in Experience.objects.filter(
        user=user,
        poste__isnull=False,
        societe__isnull=False,
        adresse_exp__isnull=False,
        date_debut__isnull=False,
        description__isnull=False
        ):
        experiences.append({
            'poste': experience.poste,
            'societe': experience.societe,
            'adresse_exp': experience.adresse_exp,
            'date_debut': experience.date_debut.strftime("%B %Y"),
            'date_fin': experience.date_fin.strftime("%B %Y"),
            'description': experience.description
        })
    
    # Récupération des formations de l'utilisateur avec leurs détails
    formations = []
    for formation in Formation.objects.filter(
        user=user,
        diplome__isnull=False,
        etablissement__isnull=False,
        adresse_formation__isnull=False,
        date_debut_formation__isnull=False
        ):
        formations.append({
            'diplome': formation.diplome,
            'etablissement': formation.etablissement,
            'adresse_formation': formation.adresse_formation,
            'date_debut_formation': formation.date_debut_formation.strftime("%B %Y"),
            'date_fin_formation': formation.date_fin_formation.strftime("%B %Y")
        })
    
    # Récupération des langues de l'utilisateur
    langue = Langue.objects.get(user=user)
    anglais = langue.anglais
    francais = langue.francais
    
    return render(request, 'pdf/cv1.html', context={'nomcv': nomcv, 'prenomcv': prenomcv, 'emailcv': emailcv, 'numero': numero, 'adresse': adresse, 'profil': profil, 'competence': competence, 'interet': interet, 'experiences': experiences, 'formations': formations, 'anglais': anglais, 'francais': francais})

def generer_cv(request):
    user = request.user
    
    # Récupération des informations personnelles
    infoperso = InfoPerso.objects.get(user=user)
    nomcv = infoperso.nomcv
    prenomcv = infoperso.prenomcv
    emailcv = infoperso.emailcv
    numero = infoperso.numero
    adresse = infoperso.adresse
    profil = infoperso.profil
    competence = infoperso.competence
    interet = infoperso.interet
    
    # Récupération des expériences de l'utilisateur avec leurs détails
    experiences = []
    for experience in Experience.objects.filter(
        user=user,
        poste__isnull=False,
        societe__isnull=False,
        adresse_exp__isnull=False,
        date_debut__isnull=False,
        description__isnull=False
        ):
        experiences.append({
            'poste': experience.poste,
            'societe': experience.societe,
            'adresse_exp': experience.adresse_exp,
            'date_debut': experience.date_debut.strftime("%B %Y"),
            'date_fin': experience.date_fin.strftime("%B %Y"),
            'description': experience.description
        })
    
    # Récupération des formations de l'utilisateur avec leurs détails
    formations = []
    for formation in Formation.objects.filter(
        user=user,
        diplome__isnull=False,
        etablissement__isnull=False,
        adresse_formation__isnull=False,
        date_debut_formation__isnull=False
        ):
        formations.append({
            'diplome': formation.diplome,
            'etablissement': formation.etablissement,
            'adresse_formation': formation.adresse_formation,
            'date_debut_formation': formation.date_debut_formation.strftime("%B %Y"),
            'date_fin_formation': formation.date_fin_formation.strftime("%B %Y")
        })
    
    # Récupération des langues de l'utilisateur
    langue = Langue.objects.get(user=user)
    anglais = langue.anglais
    francais = langue.francais
    
    # template= get_template('pdf/cv1.html')
    # context={'nomcv': nomcv, 'prenomcv': prenomcv, 'emailcv': emailcv, 'numero': numero, 'adresse': adresse, 'profil': profil, 'competence': competence, 'interet': interet, 'experiences': experiences, 'formations': formations, 'anglais': anglais, 'francais': francais}
    # html = template.render(context)
    # options = {
    #     'page-size': 'Letter',
    #     'encoding': 'UTF-8',
    # }
    # pdf = pdfkit.from_string(html, False, options)

    # reponse = HttpResponse(pdf, content_type='application/pdf')
    # reponse['Content-Disposition']="attachement"
    template = get_template('pdf/cv1.html')
    html_content = template.render({
        'nomcv': nomcv,
        'prenomcv': prenomcv,
        'emailcv': emailcv,
        'numero': numero,
        'adresse': adresse,
        'profil': profil,
        'competence': competence,
        'interet': interet,
        'experiences': experiences,
        'formations': formations,
        'anglais': anglais,
        'francais': francais
    })

    # Conversion de la page HTML en PDF
    pdf = pdfkit.from_string(html_content, False)
    
    # Réponse HTTP avec le PDF en pièce jointe
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="cv.pdf"'
    
    return response
   

def dashboard(request):
    return render(request, 'pdf/dashboard.html')

def update_cv(request):
    user = request.user
    
    if request.method == 'POST':
        # Récupération des données du formulaire
        nomcv = request.POST.get('nomcv')
        prenomcv = request.POST.get('prenomcv')
        emailcv = request.POST.get('emailcv')
        numero = request.POST.get('numero')
        adresse = request.POST.get('adresse')
        profil = request.POST.get('profil')
        competence = request.POST.get('competence')
        interet = request.POST.get('interet')
        
        # Mise à jour des informations personnelles de l'utilisateur
        InfoPerso.objects.filter(user=user).update(
            nomcv=nomcv,
            prenomcv=prenomcv,
            emailcv=emailcv,
            numero=numero,
            adresse=adresse,
            profil=profil,
            competence=competence,
            interet=interet
        )
        
        # Mise à jour des expériences de l'utilisateur
        experiences_count = int(request.POST.get('experiences_count', 0))
        for i in range(1, experiences_count + 1):
            poste = request.POST.get(f'poste{i}')
            societe = request.POST.get(f'societe{i}')
            adresse_exp = request.POST.get(f'adresse_exp{i}')
            date_debut = request.POST.get(f'date_debut{i}')
            date_fin = request.POST.get(f'date_fin{i}')
            description = request.POST.get(f'description{i}')
            
            Experience.objects.update_or_create(
                user=user,
                poste=poste,
                societe=societe,
                adresse_exp=adresse_exp,
                date_debut=date_debut,
                date_fin=date_fin,
                description=description
            )
        
        # Mise à jour des formations de l'utilisateur
        formations_count = int(request.POST.get('formations_count', 0))
        for i in range(1, formations_count + 1):
            diplome = request.POST.get(f'diplome{i}')
            etablissement = request.POST.get(f'etablissement{i}')
            adresse_formation = request.POST.get(f'adresse_formation{i}')
            date_debut_formation = request.POST.get(f'date_debut_formation{i}')
            date_fin_formation = request.POST.get(f'date_fin_formation{i}')
            
            Formation.objects.update_or_create(
                user=user,
                diplome=diplome,
                etablissement=etablissement,
                adresse_formation=adresse_formation,
                date_debut_formation=date_debut_formation,
                date_fin_formation=date_fin_formation
            )
        
        # Mise à jour des compétences linguistiques de l'utilisateur
        anglais = request.POST.get('anglais')
        francais = request.POST.get('francais')
        Langue.objects.filter(user=user).update(
            anglais=anglais,
            francais=francais
        )
        
        # Rediriger l'utilisateur vers une page de confirmation ou une autre page appropriée
        return redirect('update_cv')  # Remplacez 'confirmation_page' par le nom de votre vue de confirmation
        
    else:
        # Si la méthode n'est pas POST, affichez simplement la page avec les données actuelles de l'utilisateur
        # Récupération des informations personnelles
        infoperso = InfoPerso.objects.get(user=user)
        nomcv = infoperso.nomcv
        prenomcv = infoperso.prenomcv
        emailcv = infoperso.emailcv
        numero = infoperso.numero
        adresse = infoperso.adresse
        profil = infoperso.profil
        competence = infoperso.competence
        interet = infoperso.interet
        
        # Récupération des expériences de l'utilisateur avec leurs détails
        experiences = []
        for experience in Experience.objects.filter(
            user=user,
            poste__isnull=False,
            societe__isnull=False,
            adresse_exp__isnull=False,
            date_debut__isnull=False,
            description__isnull=False
            ):
            experiences.append({
                'poste': experience.poste,
                'societe': experience.societe,
                'adresse_exp': experience.adresse_exp,
                'date_debut': experience.date_debut,
                'date_fin': experience.date_fin,
                'description': experience.description
            })        
        # Récupération des formations de l'utilisateur avec leurs détails
        formations = []
        for formation in Formation.objects.filter(
            user=user,
            diplome__isnull=False,
            etablissement__isnull=False,
            adresse_formation__isnull=False,
            date_debut_formation__isnull=False
            ):
            formations.append({
                'diplome': formation.diplome,
                'etablissement': formation.etablissement,
                'adresse_formation': formation.adresse_formation,
                'date_debut_formation': formation.date_debut_formation,
                'date_fin_formation': formation.date_fin_formation
            })
            
        # Récupération des langues de l'utilisateur
        langue = Langue.objects.get(user=user)
        anglais = langue.anglais
        francais = langue.francais
        
        return render(request, 'pdf/updatecv.html', context={'nomcv': nomcv, 'prenomcv': prenomcv, 'emailcv': emailcv, 'numero': numero, 'adresse': adresse, 'profil': profil, 'competence': competence, 'interet': interet, 'experiences': experiences, 'formations': formations, 'anglais': anglais, 'francais': francais})  

def supprimer_cv(request):
    user = request.user
    
    InfoPerso.objects.filter(user=user).delete()
    
    Experience.objects.filter(user=user).delete()
    
    Formation.objects.filter(user=user).delete()
    
    Langue.objects.filter(user=user).delete()
    
    return redirect('index')  # Remplacez 'index' par le nom de la vue vers laquelle vous souhaitez rediriger l'utilisateur après la suppression du CV        