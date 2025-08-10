from django.db import models

# Create your models here.

class Type_Player(models.Model):
    type_name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = "type_player"
        verbose_name_plural = "Type Players"


    def __str__(self):
        return self.type_name


class Player(models.Model):
    nickname = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    nationality = models.CharField(max_length=50)
    type_player = models.ForeignKey(Type_Player, on_delete=models.CASCADE, related_name="type_player")    

    class Meta:
        managed = True
        db_table = "player"
        verbose_name_plural = "Players"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Team(models.Model):
    team_name = models.CharField(max_length=50, unique=True)
    country = models.CharField(max_length=50)
    world_ranking = models.PositiveIntegerField()
    valve_ranking = models.PositiveIntegerField()
    coach = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="coach")
    players = models.ManyToManyField(Player, related_name="players")

    class Meta:
        managed = True
        db_table = "team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return self.team_name



