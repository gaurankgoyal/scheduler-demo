from django.shortcuts import render

posts = [
    {
        'author': 'CoreyMS',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'August 28, 2018'
    }
]


def home(request):
    context = {
        'posts': posts,
        'title': 'Awesome'
    }
    return render(request, 'scheduler/home.html', context)


def about(request):
    return render(request, 'scheduler/about.html')


def add_account(request):
    return render(request, 'scheduler/add-account.html')
