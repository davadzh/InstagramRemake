from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import View, RedirectView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from .models import Publication, Profile_info, Notification, Comment
from django.contrib.auth.models import User
from .forms import PublicationForm, Profile_InfoForm, CommentForm

from django.template.loader import render_to_string
from django.http import JsonResponse
import json

from datetime import datetime

# Create your views here.

def indexView(request):
    return render(request, 'index.html')


@login_required
def feedView(request):
    user_info = get_object_or_404(Profile_info, username=request.user.id)
    feed_pubs = Publication.objects.order_by('-pub_date')[:100]
    return render(request, 'feed.html', context={'feed_pubs': feed_pubs, 'user_info': user_info})


class PostCreate(LoginRequiredMixin, View):
    def get(self, request):
        form = PublicationForm
        return render(request, 'create_post.html', context={'form': form})

    def post(self, request):
        # Заменяем в словаре значение id автора с дефолтного на юзер id
        a_id = str(request.user.id)
        request.POST = request.POST.copy()
        request.POST.update({'author': a_id})
        bound_form = PublicationForm(request.POST, request.FILES)
        if bound_form.is_valid():
            new_post = bound_form.save()
            return redirect('/profile/' + request.user.username)
        return render(request, 'create_post.html', context={'form': bound_form})


class ProfileEdit(LoginRequiredMixin, UpdateView):
    def get(self, request):
        form = Profile_InfoForm
        return render(request, 'profile_edit.html', context={'form': form})

    def post(self, request):
        # Заменяем в словаре значение id автора с дефолтного на юзер id
        a_id = str(request.user.id)
        request.POST = request.POST.copy()
        request.POST.update({'username': a_id})
        bound_form = Profile_InfoForm(request.POST, request.FILES)
        current_data = Profile_info.objects.filter(username = a_id)
        current_data.delete()
        if bound_form.is_valid():
            profile_edited = bound_form.save()
            return redirect('/profile/' + request.user.username)
        return render(request, 'profile_edit.html', context={'form': bound_form})



@login_required
def recomendView(request):
    all_pubs = Publication.objects.order_by('-pub_date')[:100]
    return render(request, 'recomend.html', context={'all_pubs': all_pubs})


@login_required
def subscription_process(request, other_user):

    other_user_ = get_object_or_404(User, id = int(other_user))

    other_user = get_object_or_404(Profile_info, username = other_user_)
    this_user = get_object_or_404(Profile_info, username = request.user.id)
    this_user_ = request.user

    is_sub = False

    if other_user_ in this_user.subscriptions.all():
        print('Отписался')
        this_user.subscriptions.remove(other_user_)
        other_user.subscribers.remove(this_user_)
        is_sub = False
        notification_unsub = Notification.objects.filter(notification_from=this_user_.username, notification_text=' подписался(-ась) на вас.')
        if notification_unsub:
            for nt in notification_unsub:
                nt.delete()
    else:
        print('Подписался')
        this_user.subscriptions.add(other_user_)
        other_user.subscribers.add(this_user_)
        is_sub = True
        notification_sub = Notification.objects.create(username=other_user_,
                                                        notification_from=this_user_.username,
                                                        notification_text=' подписался(-ась) на вас.')        
            
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

@login_required
def like_post(request):
    all_pubs = Publication.objects.order_by('-pub_date')[:100]
    user = request.user
    # obj = Publication.objects.get(id=request.POST.get('post_id'))
    obj = get_object_or_404(Publication, id=request.POST.get('post_id'))

    is_liked = False
    if user.is_authenticated:
        if user in obj.pub_likes.all():
            obj.pub_likes.remove(user)
            is_liked = False
            if user.username != obj.author.username:
                notification_unlike = Notification.objects.get(notification_from=user.username, 
                                                                notification_text=' нравится ваше фото.', 
                                                                pub_id=obj.id)
                if notification_unlike:
                    notification_unlike.delete()
        else:
            print(user.username)
            print(obj.author.username)
            obj.pub_likes.add(user)
            is_liked = True
            if user.username != obj.author.username:
                notification_like = Notification.objects.create(username=obj.author,
                                                            notification_from=user.username,
                                                            notification_text=' нравится ваше фото.',
                                                            pub_id=obj.id)

    context = {
        'obj': obj,
        'is_liked': is_liked,
        'total_likes': obj.total_likes()
    }
    # if request.is_ajax():
    #     html = render_to_string('like_button.html', context, request=request)
    #     return JsonResponse({'form': html})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # return render(request, 'recomend.html', {'all_pubs': all_pubs, 'is_liked': is_liked, 'current_p_id': request.POST.get('post_id')})


@login_required
def notificationsView(request):
    nots = Notification.objects.filter(username=request.user).order_by('-not_date')[:30]
    return render(request, 'notifications.html', context={'nots': nots})


@login_required
def profileView(request, usname):
    current_user_User = get_object_or_404(User, username=usname)
    current_user = get_object_or_404(Profile_info, username=current_user_User.id)
    all_pubs = Publication.objects.filter(author = current_user_User.id).order_by('-pub_date')[:100]
    return render(request, 'profile.html', context={'all_pubs': all_pubs, 'current_user': current_user})


@login_required
def publicationView(request, pub_id):
    comments_of_pub = Comment.objects.filter(pub=pub_id).order_by('-comment_date')
    publication = get_object_or_404(Publication, id=pub_id)
    current_user = get_object_or_404(User, username=publication.author.username)
    comment_form = CommentForm
    context = { 
        'pub': publication,
        'current_user': current_user,
        'comment_form': comment_form,
        'comments_of_pub': comments_of_pub
    }
    if request.POST:
        a_id = str(request.user.id)
        p_id = str(pub_id)
        request.POST = request.POST.copy()
        request.POST.update({'author': a_id, 'pub': pub_id})
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'publication.html', context=context)



def registerView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() 
            reg_user = get_object_or_404(User, username = request.POST.get('username'))
            # reg_user = User.objects.filter(username = request.POST.get('username'))
            # Создание поля в таблице для кастомных значений юзера
            initial = {'username': reg_user}
            form_info = Profile_InfoForm(initial)
            if form_info.is_valid():
                form_info.save()
            return redirect('login_url')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
