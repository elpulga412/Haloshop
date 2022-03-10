from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    # full_name = forms.CharField(required=True)
    # phone = forms.CharField(required=True)
    # address = forms.CharField(required=True)
    # state = forms.CharField(required=True)
    # city = forms.CharField(required=True)
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={"name":"note", "placeholder":"Ghi chú", "cols":'10', 'rows':'4'}))
    class Meta:
        model = Order
        fields = ["full_name", "phone", "address", "state", "city", "note"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update({"id":"full_name", "name":"fullname", "placeholder":"Nguyen Van A", 'required': True})
        self.fields["phone"].widget.attrs.update({"id":"phone", "name":"phone", "placeholder":"090...", 'required': True})
        self.fields["address"].widget.attrs.update({"id":"address", "name":"Địa chỉ", "placeholder":"Số 6 - Lê Văn Thiêm", 'required': True})
        self.fields["state"].widget.attrs.update({"id":"state", "name":"state", "placeholder":"Thanh Xuân", 'required': True })
        self.fields["city"].widget.attrs.update({"id":"city", "name":"city", "placeholder":"Hà Nội", 'required': True})