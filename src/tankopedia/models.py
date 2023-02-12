from django.db import models


class Nation(models.Model):
    name = models.CharField(max_length=255, primary_key=True, unique=True)
    image = models.ImageField(upload_to='nations', null=True, blank=True)

    def __str__(self):
        return self.name


class TankType(models.Model):
    name = models.CharField(max_length=255, primary_key=True, unique=True)
    image = models.ImageField(upload_to='tank_types', null=True, blank=True)

    def __str__(self):
        return self.name


class Tank(models.Model):

    # basic infos about tank
    tank_id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    # tank tech tree infos
    tier = models.IntegerField()
    nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
    type = models.ForeignKey(TankType, on_delete=models.CASCADE)
    is_premium = models.BooleanField()
    is_gift = models.BooleanField()
    is_premium_igr = models.BooleanField()
    is_wheeled = models.BooleanField()

    def __str__(self):
        return self.name


class TankImage(models.Model):
    tank = models.ForeignKey(
        Tank, on_delete=models.CASCADE, related_name='images')
    name = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return f'{self.tank.name} - {self.name}'

    class Meta:
        unique_together = ('tank', 'name',)
