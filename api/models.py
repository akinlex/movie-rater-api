from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator


class MyUserManager(BaseUserManager):
	def create_user(self, email, password=None, **kwargs):
		"""
		Creates and saves a User with the given email, date of
		birth and password.
		"""
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			email=self.normalize_email(email),
			**kwargs
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password=None, **kwargs):
		"""
		Creates and saves a superuser with the given email, date of
		birth and password.
		"""
		# kwargs.setdefault('is_staff', True)
		kwargs.setdefault('is_superuser', True)
		kwargs.setdefault('is_active', True)

		user = self.create_user(
			email,
			password=password,
			**kwargs
		)

		user.is_admin = True
		user.save(using=self._db)
		return user

class CustomUser(AbstractUser):
	email = models.EmailField(max_length=255, unique=True)
	username = None     
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = MyUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	def __str__(self):
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

class MUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, 
		on_delete=models.CASCADE, related_name='details')
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.last_name


class Movie(models.Model):
	GENRE = (
		('Drama', 'Drama'),
		('Comedy', 'Comedy'),
		('Romance', 'Romance'),
		('Adventure', 'Adventure'),
		('Sci-fi', 'Sci-fi'),
	)

	title = models.CharField(max_length=40)
	summary = models.TextField(max_length=300)
	director = models.CharField(max_length=60)
	is_released = models.BooleanField(default=True)
	genre = models.CharField(max_length=60, choices=GENRE)
	date_released = models.DateField()
	movie_length = models.CharField(max_length=60)

	def num_of_ratings(self):
		ratings = Rating.objects.filter(movie=self)
		return len(ratings)
	
	def avg_ratings(self):
		sum = 0
		ratings = Rating.objects.filter(movie=self)

		for i in ratings:
			sum += i.stars
		
		if len(ratings) > 0:
			average = sum / len(ratings)
		else:
			return 0
		return average

	def __str__(self):
		return self.title

class Cast(models.Model):
	AWARDS = (
		('AMVCA', 'AMVCA'),
		('MAMA', 'MAMA'),
	)

	name = models.CharField(max_length=60)
	featured_movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='cast')
	awards_won = models.CharField(max_length=60, choices=AWARDS, blank=True, null=True)
	role_played = models.CharField(max_length=60)

	def __str__(self):
		return self.name

class Rating(models.Model):
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='rating')
	user = models.ForeignKey(MUser, on_delete=models.CASCADE)
	stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
	
	class Meta:
		unique_together = (('user', 'movie'),)
		index_together = (('user', 'movie'),)

	def __str__(self):
		return str(self.stars)