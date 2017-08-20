from rest_framework import serializers
from .models import Game
from django.utils import timezone

class GameSerializer(serializers.ModelSerializer):
	class Meta:
		model = Game
		fields = ('id','name', 'release_date', 'game_category')

	def validate_name(self, field):
		list_of_names = Game.objects.all().values('name')
		for n in list_of_names:
			if field == n['name']:
				raise serializers.ValidationError('Já existe um jogo com esse nome')
		if field == None or field == "":
			raise serializers.ValidationError('O nome não pode ser nulo')
		return field

	def validate_game_category(self, field):
		if field == None or field == "":
			raise serializers.ValidationError('A categoria não pode ser nula')
		return field

	def validate_release_date(self, field):
		if field == None or field == "":
			raise serializers.ValidationError('A data de lançamento não pode ser nula')
		return field

	def can_delete(self, date):
		if not timezone.now() > date:
			raise serializers.ValidationError('O jogo não pode ser deletado antes de ser lançado')
		return True
