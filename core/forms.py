from django import forms
from .models import Profile,Post,Comment,Story

class ProfileForm(forms.ModelForm):
          class Meta:
                  model=Profile
                  fields=['bio','profile_pic']

class PostForm(forms.ModelForm):
         class Meta:
                 model=Post
                 fields=['image','caption']
class CommentForm(forms.ModelForm):
         class Meta:
                 model=Comment
                 fields=['text']
                 widgets={
                         'text': forms.TextInput(attrs={'placeholder':'Add a Comm....'})
                 }
class StoryForm(forms.ModelForm):
         class Meta:
                 model=Story
                 fields=['image','caption']
                 
        