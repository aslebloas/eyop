from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(null=True, blank=True, max_length=32)
    last_name = models.CharField(null=True, blank=True, max_length=32)
    city = models.CharField(null=True, blank=True, max_length=32)
    Relationships = models.ManyToManyField(
        'self', through='Relationship', symmetrical=False, related_name='related_to+')

    def __str__(self):
        return f'{self.user.username}'


RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Following'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
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


class Code(models.Model):
    code = models.CharField(max_length=256)
    amount = models.IntegerField()
    UOM = models.CharField(max_length=8)  # unit of measure
    criteria = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.code


class Brand(models.Model):
    brand_name = models.CharField(max_length=128)
    url_pattern = models.CharField(max_length=256, blank=True, null=True)
    logo = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.brand_name
