import requests
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(null=True, blank=True, max_length=32)
    last_name = models.CharField(null=True, blank=True, max_length=32)
    city = models.CharField(null=True, blank=True, max_length=32)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    Relationships = models.ManyToManyField(
        'self', through='Relationship', symmetrical=False, related_name='related_to+')

    def __str__(self):
        return f'{self.user.username}'


RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_PENDING = 3
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Following'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
    (RELATIONSHIP_BLOCKED, 'Pending'),
)


class Relationship(models.Model):
    from_person = models.ForeignKey(
        Profile, related_name='from_people', on_delete=models.CASCADE)
    to_person = models.ForeignKey(
        Profile, related_name='to_people', on_delete=models.CASCADE)
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES)

    def add_relationship(self, person, status, symm=True):
        relationship, created = Relationship.objects.get_or_create(
            from_person=self,
            to_person=person,
            status=status)
        if symm:
            # avoid recursion by passing `symm=False`
            person.add_relationship(self, status, False)
        return relationship

    def remove_relationship(self, person, status, symm=True):
        Relationship.objects.filter(
            from_person=self,
            to_person=person,
            status=status).delete()
        if symm:
            # avoid recursion by passing `symm=False`
            person.remove_relationship(self, status, False)

    def get_relationships(self, status):
        return self.relationships.filter(
            to_people__status=status,
            to_people__from_person=self)


class Brand(models.Model):
    brand_name = models.CharField(max_length=128)
    url_pattern = models.CharField(max_length=256, blank=True, null=True)
    logo = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.brand_name


class Code(models.Model):
    code = models.CharField(max_length=256)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    amount = models.IntegerField()
    UOM = models.CharField(max_length=8)  # unit of measure
    criteria = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class Invitation(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    code = models.CharField(max_length=20)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.sender.username

    def send(self):
        return requests.post(
            settings.MAILGUN_API_URL,
            auth=("api", settings.MAILGUN_API_KEY),
            data={"from": settings.EMAIL_FROM,
                  "to": [self.email],
                  "subject": "{} is inviting you to Referral Mate!".format(
                      self.sender.username),
                  "text": "Conncect here: https://referral-mate.online/register?sender={}".format(self.sender.username)})  # noqa
