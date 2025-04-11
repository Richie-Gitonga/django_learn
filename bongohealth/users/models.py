from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

# Create your models here.

"""
    TODO:   create a custom user model for both authors and users
            create models to show additional info for authors: edu, exp
            give authors is_staff attribute to use admin pages...
            ...<limit to blog creation only> <check how to do permissions>
"""
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    date_of_birth = models.DateField(
        blank=True, null=True
    )
    photo = models.ImageField(
        upload_to='users/%Y/%m/%d/',
        blank=True
    )

    def __str__(self):
        return f'{self.user.username}\'s profile'

class Follow(models.Model):
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='rel_from_set',
        on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='rel_to_set',
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_from.username} follows {self.user_to.username}'
        
# Add the follow field to user dynamically
user_model = get_user_model()
user_model.add_to_class(
    'following',
    models.ManyToManyField(
        'self',
        through=Follow,
        related_name='followers',
        symmetrical=False
    )
)