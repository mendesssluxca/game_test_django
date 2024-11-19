from django.db import models

# Create your models here.
from django.db import models

class Player(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.username

class Score(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="scores")
    score = models.IntegerField()
    phase = models.IntegerField()  # Fase do jogo
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.username} - {self.score} pontos"
