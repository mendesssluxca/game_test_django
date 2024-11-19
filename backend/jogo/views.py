from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Player, Score

class SubmitScoreAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        score = request.data.get('score')
        phase = request.data.get('phase')

        # Procura ou cria o jogador
        player, created = Player.objects.get_or_create(username=username)

        # Salva a pontuação
        Score.objects.create(player=player, score=score, phase=phase)

        return Response({"message": "Pontuação salva com sucesso!"}, status=status.HTTP_201_CREATED)
