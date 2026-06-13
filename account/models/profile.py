from django.db import models

class Profile(models.Model):
    user=models.OneToOneField('account.CustomUser',on_delete=models.CASCADE,related_name="profile")
    first_name=models.CharField(max_length=255,blank=True,null=True)
    last_name=models.CharField(max_length=255,blank=True,null=True)
    bio=models.TextField(max_length=255,blank=True,null=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name()