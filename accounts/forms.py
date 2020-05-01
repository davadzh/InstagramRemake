from django import forms
from .models import Publication, Profile_info, Comment
from django.core.exceptions import ValidationError


class LikeForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['author']


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['author', 'pub_text', 'pub_pic']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'pub', 'comment_text']

    
class Profile_InfoForm(forms.ModelForm):
    class Meta:
        model = Profile_info
        fields = ['username', 'name', 'phone', 'email', 'profile_pic', 'subscribers', 'subscriptions']

    # def save(self):
    #     new_publication = Publication.objects.create(
    #         pub_text=self.cleaned_data['pub_text']
    #     )
    #     return new_publication