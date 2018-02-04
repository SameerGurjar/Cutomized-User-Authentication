from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, gender, phone_number):

        if not email:
            raise ValueError('Users must have an email address')

        if not first_name:
            raise ValueError('first name required')

        if not last_name:
            raise ValueError('last name required')

        if gender is None:
            raise ValueError('Gender required')

        if phone_number is None:
            raise ValueError('phone_number required')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            gender=gender
        )

        user.save(using=self._db)
        return user


    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not first_name:
            raise ValueError('first name required')

        if not last_name:
            raise ValueError('last name required')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            gender=None,
            phone_number=None,
        )

        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    MALE = 'M'
    FEMALE = 'F'
    GENDER = ((MALE,'MALE'),(FEMALE,'FEMALE'))


    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=100, verbose_name='First Name')
    last_name = models.CharField(max_length=100, verbose_name='Last Name')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{12}$',
                        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, null=True)
    gender = models.CharField(choices=GENDER, max_length=1, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # last_login is only used to fix the error for login() function as it sends signal user_logged_in
    last_login = models.DateTimeField(null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        fullname = self.first_name + ' ' + self.last_name
        # The user is identified by their email address
        return fullname

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

