from django.db import models
from django_countries.fields import CountryField
from django.utils.timezone import now 
from django.contrib.auth.models import User 


class License(models.Model):
	name = models.CharField(max_length=149, unique=True)
	pricing = models.DecimalField(max_digits=9, decimal_places=2,default=0.0)
	duration = models.IntegerField()
	release_data = models.DateField(default= now)

	def __str__(self):
		return self.name


class Code(models.Model):
	code = models.CharField(max_length=149, unique=True)
	validity_begins = models.DateField(default=now)
	validity_expires = models.DateField(default= now)
	license = models.ForeignKey(License, related_name='code_license', on_delete=models.CASCADE, blank=True, null=True,default=1)
	is_event_code = models.BooleanField(default=False)

	def __str__(self):
		return self.code

# hidden model
# class Profile(models.Model):
# 	# country = CountryField(blank=True, null=True)
# 	picture = models.FileField(upload_to='pics/', blank=True, null=True)
# 	user = models.OneToOneField(User, on_delete=models.CASCADE)
# 	code = models.ForeignKey(Code, related_name='user_code', on_delete=models.CASCADE,null=True)

# 	def __str__(self):
# 		return self.user.username

# el nucleo del sistema de autenticacion
class User_Code(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)  # unique=True)
	code = models.ForeignKey(Code, on_delete=models.CASCADE)#, unique=True)

	def __str__(self):
		return str(self.user.username + '_' + self.code.code)


class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user', on_delete=models.CASCADE)
    # user = models.ForeignKey(User, related_name='logged_in_user', on_delete=models.CASCADE, unique=True) 
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return str(self.user.username+"-"+str(self.session_key))