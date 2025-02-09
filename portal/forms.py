from django import forms
from .models import Comment
from .models import Post,Category


class NewCommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ["content"]
        widgets={
            "content":forms.Textarea(attrs={"class":"form-control"}),

        }
    

choices=Category.objects.all().values_list('name', 'name')

choice_list=[]
for item in choices:
    choice_list.append(item)


class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','content','excerpt','image','category']
        widgets={
            'title':forms.TextInput(attrs={"class":"form-control"}),
            'category':forms.Select(choices=choice_list , attrs={'class': 'form-control'}),
            'content':forms.Textarea(attrs={"class":"form-control"}),
            'excerpt':forms.Textarea(attrs={"class":"form-control"}),
            'image':forms.ClearableFileInput(attrs={"class": "form-control-file"}),  
            
        }


class PostSearchForm(forms.Form):
    q =forms.CharField()
    c=forms.ModelChoiceField(
        queryset=Category.objects.all().order_by('name'))
    

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['c'].label = ''
        self.fields['c'].required = False
        self.fields['c'].label = 'Category'
        self.fields['q'].label = 'Search For'
        self.fields['q'].widget.attrs.update(
            {'class': 'form-control'})




