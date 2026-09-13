from django import forms

from .models import Comment, Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        labels = {'avatar': 'New picture'}
        widgets = {
            'avatar': forms.FileInput(attrs={'accept': 'image/*'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': 'Your comment'}
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Share your thoughts about this mod...',
                'maxlength': 2000,
            }),
        }