from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.widgets import CKEditorWidget
from .models import *
from category.models import *
from ckeditor.fields import RichTextField

class VersionAdminForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

class ReviewRatingForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = "__all__"

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['id','version', 'capacity', 'price', 'is_active']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['version'].widget.attrs.update({'required': True})

class VersionForm(forms.ModelForm):

    class Meta:
        model = Version
        fields = ["category", "series", "name", "image", "description"]
    
    def __init__(self, *args, **kwargs):
        super(VersionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            class_name = 'cls_' + field
            self.fields[field].widget.attrs.update({'class': class_name})
    

class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ["category", "name"]
    
    def __init__(self, *args, **kwargs):
        super(SeriesForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            class_name = 'cls_' + field
            self.fields[field].widget.attrs.update({'class': class_name, 'required': True})


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ["name", "image", "description"]
    
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'required': True})

class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = ["product", "color", "image", "stock", "is_available"]