import io, math
from uuid import uuid4
from PIL import Image, UnidentifiedImageError
from django import forms
from django.core.files.base import ContentFile
from .models import FieldReport, Advisory

class ReportForm(forms.ModelForm):
    class Meta:
        model = FieldReport
        fields = ['kind','description','latitude','longitude','photo']
        widgets = {'description': forms.Textarea(attrs={'rows':3}), 'latitude':forms.NumberInput(attrs={'step':'any'}), 'longitude':forms.NumberInput(attrs={'step':'any'})}
    def clean(self):
        data = super().clean()
        lat,lon = data.get('latitude'),data.get('longitude')
        if (lat is None) != (lon is None):
            raise forms.ValidationError('Provide both coordinates or leave both blank.')
        if lat is not None and (not math.isfinite(lat) or not math.isfinite(lon) or not -90 <= lat <= 90 or not -180 <= lon <= 180):
            raise forms.ValidationError('Invalid coordinates.')
        return data
    def clean_photo(self):
        upload = self.cleaned_data.get('photo')
        if not upload: return upload
        if upload.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Photo must be 5 MB or smaller.')
        try:
            with Image.open(upload) as image:
                if image.format not in ['JPEG','PNG'] or image.width*image.height > 20000000:
                    raise forms.ValidationError('Use a JPEG/PNG up to 20 megapixels.')
                image.load()
                image = image.convert('RGB')
                image.thumbnail((1600,1600))
                out = io.BytesIO()
                image.save(out,format='JPEG',quality=85)
        except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError):
            raise forms.ValidationError('The photo could not be read.')
        return ContentFile(out.getvalue(), name=f'{uuid4().hex}.jpg')

class AdvisoryForm(forms.ModelForm):
    hours = forms.IntegerField(min_value=1,max_value=48,initial=12,label='Expires after hours')
    class Meta:
        model = Advisory
        fields = ['kind','title','message']
        widgets = {'message': forms.Textarea(attrs={'rows':3})}

class TriageForm(forms.Form):
    status = forms.ChoiceField(choices=FieldReport._meta.get_field('status').choices)
    verified = forms.BooleanField(required=False,label='Report reviewed and verified')
    assign_to_me = forms.BooleanField(required=False,label='Assign to me')
    note = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows':2}))
    version = forms.IntegerField(min_value=1,widget=forms.HiddenInput)
