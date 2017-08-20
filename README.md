# GamesAPI
Este projeto tem como objetivo realizar uma comparação entre a implementação de validação na diretamente na View ou usilizar métodos de validação no Django Rest Framework.

# Validações na View
Esse tipo de validação é realizada diretamente nas implementações de funções. Ela consiste em analisar os dados da requisição, seja ela um POST ou um PUT e verificar se esses dados são válidos. Caso contrário, será retornado um erro com uma informação do que está errado.
Este exemplo implementa Django Rest Framework e os dados das requisições são recebidos em JSON. Para se verifica cada um dos dados da requisição, se utiliza *request.data* ao ivés de *request.POST*.
Este é um método que avalia os campos nulos:
```python
def not_null_validation(nome_campo, campo):
	if campo == None or campo == "":
		return False
	return True
```
Implementação:
```python
if request.method == 'POST':
		if not not_null_validation('name', request.data.get('name')):
			return Response("name não pode ser nulo", status=status.HTTP_400_BAD_REQUEST)
		if not not_null_validation('game_category', request.data.get('game_category')):
			return Response("game_category não pode ser nulo", status=status.HTTP_400_BAD_REQUEST)
		if not not_null_validation('release_date', request.data.get('release_date')):
			return Response("release_date não pode ser nulo", status=status.HTTP_400_BAD_REQUEST)
```

# Validação com Django Rest Framework
Esse tipo de validação funciona a partir de métodos criados dentro da classe *serializer* correspondente à classe modelo.
Para implmenetar uma validação, basta criar um método que inicie com **validate_** e o nome do atributo da classe modelo que o *serializer* está tratando.
```python
def validate_name(self, field):
		list_of_names = Game.objects.all().values('name')
		for n in list_of_names:
			if field == n['name']:
				raise serializers.ValidationError('Já existe um jogo com esse nome')
		if field == None or field == "":
			raise serializers.ValidationError('O nome não pode ser nulo')
		return field
```
## Dicussão:
A utilização de validação na view é explicita e intuitiva e pode ser usada django sem necessidade de qualquer outra API, biblioteca ou framework. Porém, dependo da quantidade de campos e regras a se valdiar, pode gerar problemas de manutenção e legibilidade.
Através do Django *Rest Framework* é possivel criar validações especificas para cada tipo de campo. A validação é feita de forma automática quando itilizado o método *is_valid()* dos objetos serializers. Essa metodologia permite um maior encapsulamento do código e maior legibilidade.
