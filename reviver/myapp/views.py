from django.shortcuts import render
from .models import Publicacao, Comentario
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from datetime import datetime
from PIL import Image
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required

def index(request):
    if  request.user.is_authenticated:
        username= request.user.username
        
        return render(request, 'home.html', {'username': username})
    

    else :
        return render(request, 'home.html', {'username': ''})
    

@login_required(login_url='/login') 
def publicate_page(request):
    username= request.user.username
    if request.method == 'GET':
        return render(request, 'publicate.html',{'username':username})
    elif request.method == 'POST':
        author = request.POST.get('author')
        tit = request.POST.get('tit')
        content = request.POST.get('content')
        file = request.FILES.get('imagem')
        #img = Image.open(file)
        #path = os.path.join(settings.BASE_DIR, f'media/{file.name}-{date.today()}.jpg')
        #img = img.save(path)
        if file.size > 20000000:
            return HttpResponse('Imagem muito grande')
        
        publicacao = Publicacao()
        #publicacao.imagem = Publicacao(title = 'Minha_Lembrança', arq=file)
        publicacao.imagem = file        
        publicacao.tit = tit
        publicacao.author = author
        publicacao.date = datetime.today()
        publicacao.content = content
        publicacao.save()
        return HttpResponseRedirect('/feed')
    else:
        return HttpResponseBadRequest()


def feed_page(request):
    context = {
        "posts": Publicacao.objects.all()[:: -1],
        "username" : request.user.username
    }
    
    return render(request, 'feed.html', context)
    
def post_page(request, id):
    post = Publicacao.objects.get(id=id)
    comentarios = Comentario.objects.filter(publicacao=post)
    username= request.user.username
    
    if request.method == 'GET':
        return render(request, 'post.html', {'post': post, 'comentarios':comentarios,'username':username})
    elif request.method == 'POST':
        author = request.POST.get('author1')
        content = request.POST.get('content1')
        comentario = Comentario()
        comentario.publicacao = post
        comentario.author = author
        comentario.date = datetime.today()
        comentario.content = content
        comentario.save()
        return render(request, 'post.html', {'post': post, 'comentarios':comentarios})
    else:
        return HttpResponseBadRequest()
    

def publ_coment_page(request, publicacao_id):
    # Recupere os comentários associados a uma publicação específica
    comentarios = Comentario.objects.filter(publicacao_id=publicacao_id)
    username : request.user.username
    return render(request, 'post.html', {'comentarios': comentarios,'username':username})


def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'incorrect_login': False
        })
    elif request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/feed')
        else:
            return render(request, 'login.html', {
                'incorrect_login': True
            })  
    else:
        return HttpResponseBadRequest()
    
@login_required(login_url='/login')   
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')


