from rest_framework.serializers import ModelSerializer, EmailField, CharField, ValidationError
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='Email Address')
    email2 = EmailField(label='Confirm Email')
    class Meta:
        model = User
        fields = [
            'email',
            'email2',
            'first_name',
            'last_name',
            'phone_number',
            'gender',
        ]

    def create(self, validated_data):
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        phone_number = validated_data['phone_number']
        gender = validated_data['gender']

        try:
            user = User(
                    email = email,
                    first_name = first_name,
                    last_name = last_name,
                    phone_number = phone_number,
                    gender = gender
                )
        except:
            raise ValidationError("User already exist")

        user.save()
        return validated_data

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data['email']
        email2 = value
        if email1 != email2:
            raise ValidationError('Email must match')
        user_qs = User.objects.filter(email=email1)
        if user_qs.exists():
            raise ValidationError('This user is already registered')
        return value


class UserLoginSerializer(ModelSerializer):
    email = EmailField(required=True)
    enter_number_email = CharField(required=True)
    otp = CharField(required=True)
    phone_number = CharField(required=True)

    class Meta:
        model = User
        fields = [
            'email',
            'phone_number',
            'enter_number_or_email'
            'otp'
        ]
# 		extra_kwargs = {
# 					'password': {'write_only': True}
# 		}
#
# 	def validate(self, data):
# 		username = data.get('username', None)
# 		email = data.get('email', None)
# 		password = data['password']
# 		user_obj = None
# 		if not username and not email:
# 			raise ValidationError('Please provide either username or password')
# 		user_qs = User.objects.filter(
# 						Q(email=email)|
# 						Q(username=username)
# 					).distinct()
# 		user_qs = user_qs.exclude(email__isnull=True).exclude(email__iexact='')
# 		print(user_qs)
# 		if user_qs.exists() and user_qs.count() == 1:
# 			user_obj = user_qs.first()
# 		else:
# 			raise ValidationError('This username/email is not valid')
# 		if user_obj:
# 			if not user_obj.check_password(password):
# 				raise ValidationError('Password Incorrect')
#
# 		data['token'] = 'SOME RANDOM TOKEN'
# 		return data
