from .models import Comment, Post, Images, FAQ, FAQAnswers
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class AnswerForm(forms.ModelForm):
    class Meta:
        model = FAQAnswers
        fields = ('body',)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ('question', 'desc')

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label= 'Image')
    class Meta:
        model = Images
        fields = ('image',)