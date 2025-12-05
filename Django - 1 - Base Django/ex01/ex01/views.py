from django.shortcuts import render


def django_view(request):
    return render(request, 'ex01/django.html')


def affichage(request):
    return render(request, 'ex01/affichage.html')


def templates(request):
    context = {
        'exemple_liste': ['Élément 1', 'Élément 2', 'Élément 3'],
        'afficher_message': True,
        'exemple_variable': 'Hello Django!',
    }
    return render(request, 'ex01/templates.html', context)
