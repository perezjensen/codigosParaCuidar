from django.shortcuts import render

# Create your views here.
def landinEmpresas(request):
    return render(request,'web/empresas.html')

def landinPersonal(request):
    return render(request,'web/index.html')