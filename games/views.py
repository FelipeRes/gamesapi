from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from games.models import Game
from games.serializers import GameSerializer
from datetime import datetime
from django.utils import timezone

@api_view(['GET','POST'])
def game_list(request):
	if request.method == 'GET':
		games = Game.objects.all()
		games_serializer = GameSerializer(games, many=True)
		return Response(games_serializer.data)
	elif request.method == 'POST':
		if not_null_validation('name', request.data.get('name')):
			return Response("name não pode ser nulo", status=status.HTTP_400_BAD_REQUEST)
		if not_null_validation('game_category', request.data.get('game_category')):
			return Response("game_category não pode ser nulo", status=status.HTTP_400_BAD_REQUEST)
		if not_null_validation('release_date', request.data.get('release_date')):
			return Response("release_date não pode ser nulo", status=status.HTTP_400_BAD_REQUEST)
		if name_validation(request.data.get('name')):
			return Response("já existe um jog com esse nome cadastrado", status=status.HTTP_400_BAD_REQUEST)

		games_serializer = GameSerializer(data=request.data)
		if games_serializer.is_valid():
			games_serializer.save()
			return Response(games_serializer.data, status=status.HTTP_201_CREATED)
		return Response(games_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT', 'POST', 'DELETE'])
def game_detail(request, pk):
	try:
		game = Game.objects.get(pk=pk)
	except Game.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		games_serializer = GameSerializer(game)
		return Response(games_serializer.data)
	elif request.method == 'PUT':
		if not_null_validation('name', request.data.get('name')):
			return Response("name não pode ser nulo", status=status.HTTP_400_BAD_REQUEST)
		if not_null_validation('game_category', request.data.get('game_category')):
			return Response("game_category não pode ser nulo", status=status.HTTP_400_BAD_REQUEST)
		if not_null_validation('release_date', request.data.get('release_date')):
			return Response("release_date não pode ser nulo", status=status.HTTP_400_BAD_REQUEST)
		if name_validation(request.data.get('name')):
			return Response("já existe um jog com esse nome cadastrado", status=status.HTTP_400_BAD_REQUEST)
		games_serializer = GameSerializer(game, data=request.data)		
		if games_serializer.is_valid():
			games_serializer.save()
			return Response(games_serializer.data)
		return Response(games_serializer.erros, status=status.HTTP_400_BAD_REQUEST)
	elif request.method == 'DELETE':
		if timezone.now() > game.release_date:
			game.delete()
			return Response(status=status.HTTP_204_NO_CONTENT)
		return Response("Você não pode deletar um jogo que ainda não foi lançado", status=status.HTTP_400_BAD_REQUEST)

def name_validation(name):
	list_of_names = Game.objects.all().values('name')
	for n in list_of_names:
		if name == n['name']:
			return True
	return False

def not_null_validation(nome_campo, campo):
	if campo == None or campo == "":
		return True
	return False