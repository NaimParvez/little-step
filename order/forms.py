from django import forms




DIVISION_CHOICES = [
    ('', 'Select Division'),
    ('Dhaka', 'Dhaka'),
    ('Chittagong', 'Chittagong'),
    ('Rajshahi', 'Rajshahi'),
    ('Khulna', 'Khulna'),
    ('Barisal', 'Barisal'),
    ('Sylhet', 'Sylhet'),
    ('Rangpur', 'Rangpur'),
    ('Mymensingh', 'Mymensingh'),
]

DISTRICT_CHOICES = [('', 'Select District')]
UPAZILA_CHOICES = [('', 'Select Upazila')]

class CheckoutForm(forms.Form):
    first_name =forms.CharField(max_length=100)
    last_name =forms.CharField(max_length=100)
    email =forms.EmailField(max_length=100)
    phone_no =forms.CharField(max_length=15)
    address =forms.CharField(widget=forms.Textarea)
    
    division = forms.ChoiceField(
        choices=DIVISION_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-group', 'id': 'division'})
    )

    district = forms.ChoiceField(
        choices=DISTRICT_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-group', 'id': 'district'})
    )

    upazila = forms.ChoiceField(
        choices=UPAZILA_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-group', 'id': 'upazila'})
    )
    
    