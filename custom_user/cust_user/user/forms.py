from django import forms
from django.contrib.auth import (
    get_user_model
)
from django.db.models import Q

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    phone_number = forms.CharField(label="10 Digit Registered Phone Number (Include country code)")
    number_or_email = forms.CharField(label='OTP Phone Number or Email')
    token = forms.CharField(label='OTP')
    # class Meta:
    #     model = User
    #     fields = [
    #         'email',
    #         'phone_number',
    #     ]
    #
    #
    # def clean(self, *args, **kwargs):
    #     email = self.cleaned_data.get("email")
    #
    #
    #     # user_qs = User.objects.filter(username=username)
    #     # if user_qs.count() == 1:
    #     #     user = user_qs.first()
    #     if email:
    #         user = authenticate(email=email)
    #         if not user:
    #             raise forms.ValidationError("This user does not exist")
    #         if not user.is_active:
    #             raise forms.ValidationError("This user is not longer active.")
    #     return super(UserLoginForm, self).clean(*args, **kwargs)


    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        phone_number = self.cleaned_data.get("phone_number")

        user = User.objects.filter(
                            Q(email=email)&
                            Q(phone_number=phone_number)
                        )
        if not user.exists():
            raise forms.ValidationError('User does not exist')

        if not user.first().is_active:
            raise forms.ValidationError('User is inactive')

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    MALE = 'M'
    FEMALE = 'F'
    GENDER = ((MALE, 'MALE'), (FEMALE, 'FEMALE'))

    email = forms.EmailField(label='Email address')
    email2 = forms.EmailField(label='Confirm Email')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField()
    gender = forms.ChoiceField(GENDER)
    phone_number = forms.CharField(label="10 Digit Registered Phone Number (Include country code)")
    class Meta:
        model = User
        fields = [
            'email',
            'email2',
            'first_name',
            'last_name',
            'gender',
            'phone_number'
        ]

    # def clean(self, *args, **kwargs):
    #     email = self.cleaned_data.get('email')
    #     email2 = self.cleaned_data.get('email2')
    #     if email != email2:
    #         raise forms.ValidationError("Emails must match")
    #     email_qs = User.objects.filter(email=email)
    #     if email_qs.exists():
    #         raise forms.ValidationError("This email has already been registered")

    #     return super(UserRegisterForm,self).clean(*args, **kwargs)

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError("Emails must match")
        return email




















