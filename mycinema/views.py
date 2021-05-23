from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import Post

posts = [
    {
        'author': 'CoreyMS',
        'title': 'Władca Pierścieni - Dwie Wieże',
        'content': 'Drużyna Pierścienia zostaje rozbita, lecz zdesperowany Frodo za wszelką cenę chce wypełnić powierzone mu zadanie. Aragorn z towarzyszami przygotowuje się, by odeprzeć atak hord Sarumana.',
        'date_posted': 'August 27, 2021'
    },

    {
        'author': 'JaneyMS',
        'title': 'Hobbit - Pustkowie Smauga',
        'content': 'Hobbit Bilbo Baggins razem z Gandalfem oraz trzynastoma krasnoludami zmierza do legowiska smoka Smauga. Bohaterowie chcą pokonać bestię i odebrać jej złoto, które ukradła.',
        'date_posted': 'August 28, 2021'
    },

]


# Create your views here.

def home(request):
    context = {
        'posts': Post.objects.all()
    }

    return render(request, 'jinja2/home.html', context)


def about(request):
    return render(request, 'jinja2/about.html',{'title': 'Mytitle'})
