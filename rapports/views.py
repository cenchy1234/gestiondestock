from django.shortcuts import render

def rapport_list(request):
    return render(request, 'rapports/rapport_list.html')
