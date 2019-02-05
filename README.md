# b2w

Usado Python e MongoDB.
API Rest aceitando get, post, put, delete
Planet attributes:
    {
        "id": 1,
        "name": "Planeta Inventado",
        "climate": "Tropical Quente",
        "terrain": "arenoso",
        "screenings": 0
    }
    screenings -> quantidade de aparições em filmes busca na api https://swapi.co/.

Busca por atributo(id, name, climate, terrain):
http://localhost:8887/sw/planet/?filter{nome_atributo}=valor_atributo

Busca por nome:
http://localhost:8887/sw/planet/?filter{name}=Planeta%20Inventado
http://localhost:8887/sw/planet/?filter{name}=Tatooine

Busca por id:
http://localhost:8887/sw/planet/2
http://localhost:8887/sw/planet/?filter{id}=2

Listagem de planetas:
http://localhost:8887/sw/planet/

Para remover só fazer um request usando method delete para url 'sw/planet/id_para_remover'
http://localhost:8887/sw/planet/4

Tests com todos funcionalidades desejadas, para rodar a bateria de tests:
sudo docker-compose run --rm api python3 manage.py test


#https://code.djangoproject.com/wiki/NoSqlSupport

#https://pythonhosted.org/django-rest-framework-mongoengine/serializers/
#https://mongoengine-odm.readthedocs.io/tutorial.html