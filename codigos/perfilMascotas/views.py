from django.shortcuts import render,HttpResponse,redirect



# Create your views here.
def ver_perfil(request):
    return render(request, 'perfilMascotas/perfil.html', {})


