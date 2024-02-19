from django.shortcuts import render
from .models import Publicacao, Comentario
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from datetime import datetime
from PIL import Image
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'home.html')

@login_required(login_url='/login') 
def publicate_page(request):
    if request.method == 'GET':
        return render(request, 'publicate.html')
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
        "posts": Publicacao.objects.all()[:: -1]
    }
    return render(request, 'feed.html', context)
    
def post_page(request, id):
    post = Publicacao.objects.get(id=id)
    return render(request, 'post.html', {'post': post})

def coment_page(request, id):
    if request.method == 'GET':
        return render(request, 'post.html')
    elif request.method == 'POST':
        author = request.POST.get('author1')
        publicacao_id = id
        content = request.POST.get('content1')
        comentario = Comentario()
        comentario.id_post = publicacao_id
        comentario.author = author
        comentario.date = datetime.today()
        comentario.content = content
        comentario.save()
        return HttpResponseRedirect('/post/<int:id>')
    else:
        return HttpResponseBadRequest()
    

def publ_coment_page(request, publicacao_id):
    # Recupere os comentários associados a uma publicação específica
    comentarios = Comentario.objects.filter(publicacao_id=publicacao_id)
    return render(request, 'post.html', {'comentarios': comentarios})


def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'incorrect_login': False
        })
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
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


