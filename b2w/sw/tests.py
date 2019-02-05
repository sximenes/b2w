import json
import requests
from django.test import TestCase
from django.test import Client

from sw.models import Planet
from sw.factories import PlanetFactory

# Create your tests here.
class PlanetModelTestCase(TestCase):
    def setUp(self):
        # Planeta Inventado screenings 0
        self.planet1 = PlanetFactory.create(
            name = 'Planeta Inventado',
            climate = 'Tropical Quente',
            terrain = 'Arenoso'
        )
        self.planet1.save()

        # Yavin IV screenings 1
        self.planet2 = PlanetFactory.create(
            name = 'Yavin IV',
            climate = 'temperate, tropical',
            terrain = 'jungle, rainforests'
        )
        self.planet2.save()

        # Tatooine screenings 5
        self.planet3 = PlanetFactory.create(
            name = 'Tatooine',
            climate = 'arid',
            terrain = 'desert'
        )
        self.planet3.save()
        

    def test_get_screenings(self):
        """
            Test method get_screenings(Amount of movies shown) on 
            api https://swapi.co/
        """
        url = 'https://swapi.co/api/planets/?search='

        # Planeta Inventado screenings 0
        expected_screenings_p1 = 0
        screenings_p1 = self.planet1.get_screenings()
        self.assertEqual(screenings_p1, expected_screenings_p1)

        # Yavin IV screenings 1
        url_request = '%s%s' %(url, self.planet2.name)
        r = requests.get(url_request, timeout=10)
        result = r.json()
        # swapi response
        expected_screenings_p2 = len(result['results'][0]['films'])
        screenings_p2 = self.planet2.get_screenings()
        self.assertEqual(screenings_p2, expected_screenings_p2)

        # Tatooine screenings 5
        url_request = '%s%s' %(url, self.planet3.name)
        r = requests.get(url_request, timeout=10)
        result = r.json()
        # swapi response
        expected_screenings_p3 = len(result['results'][0]['films'])
        screenings_p3 = self.planet3.get_screenings()
        self.assertEqual(screenings_p3, expected_screenings_p3)


class PlanetAPITestCase(TestCase):
    def setUp(self):
        # Planeta Inventado screenings 0
        self.planet1 = PlanetFactory.create(
            name = 'Planeta Inventado',
            climate = 'Tropical Quente',
            terrain = 'Arenoso'
        )
        self.planet1.save()

        # Yavin IV screenings 1
        self.planet2 = PlanetFactory.create(
            name = 'Yavin IV',
            climate = 'temperate, tropical',
            terrain = 'jungle, rainforests'
        )
        self.planet2.save()

        # Tatooine screenings 5
        self.planet3 = PlanetFactory.create(
            name = 'Tatooine',
            climate = 'arid',
            terrain = 'desert'
        )
        self.planet3.save()
        

    def test_planet_attributes_api_get(self):
        """
            Test atrributes of planet returned of API:
            {   "id": 1,
                "name": "Planeta Inventado",
                "climate": "Tropical Quente",
                "terrain": "arenoso",
                "screenings": 0
            }
            screenings -> Amount of movies shown
        """
        c = Client()
        url = '/sw/planet/%s' % self.planet1.id

        # Get Data
        result = c.get(url)
        data = json.loads(result.content)['planet']

        atributes = ['id', 'name', 'climate', 'terrain', 'screenings']
        for attribute in atributes:
            self.assertTrue(attribute in data)

    def test_add_planet_api_post(self):
        """
            Test POST API to add planet with:
                - name
                - climate
                - terrain 
        """
        # before add Total 3 planets
        self.assertEqual(Planet.objects.count(), 3)

        c = Client()
        url = '/sw/planet/'
        # screenings 3
        planet_data = {
            'name': 'Dagobah',
            'climate': 'murky',
            'terrain': 'swamp, jungles'
            }
        # Post
        result = c.post(url, data=planet_data)

        planet_created = json.loads(result.content)['planet']
        # screenings 3
        self.assertEqual(planet_created['screenings'], 3)

        # after Total 4 planets
        self.assertEqual(Planet.objects.count(), 4)

        planet = Planet.objects.get(id=planet_created['id'])
        self.assertEqual(planet.name, 'Dagobah')
        self.assertEqual(planet.climate, 'murky')
        self.assertEqual(planet.terrain, 'swamp, jungles')

    def test_list_planets(self):
        """
            Test list of planets :
        """
        c = Client()
        url = '/sw/planet/'

        # Get Data
        result = c.get(url)
        planet_list = json.loads(result.content)['planets']
        # Total 3 planets
        self.assertEqual(len(planet_list), Planet.objects.count())
        self.assertEqual(len(planet_list), 3)
        self.assertTrue(isinstance(planet_list, list))
        self.assertTrue(isinstance(planet_list[0], dict))

        atributes = ['id', 'name', 'climate', 'terrain', 'screenings']
        for attribute in atributes:
            self.assertTrue(attribute in planet_list[0])

    def test_get_by_name(self):
        """
            Test get filter planet by name.
        """
        c = Client()
        url = '/sw/planet/?filter{name}=%s' % self.planet3.name

        # Get Data
        result = c.get(url)
        planet_list = json.loads(result.content)['planets']
        # Total 1 planets
        self.assertTrue(isinstance(planet_list, list))
        self.assertEqual(len(planet_list), 1)
        self.assertTrue(isinstance(planet_list[0], dict))

        planet = planet_list[0]
        self.assertEqual(planet['id'], self.planet3.id)
        self.assertEqual(planet['name'], self.planet3.name)
        self.assertEqual(planet['climate'], self.planet3.climate)
        self.assertEqual(planet['terrain'], self.planet3.terrain)
        self.assertEqual(planet['screenings'], self.planet3.get_screenings())

    def test_get_by_id(self):
        """
            Test get planet by id.
        """
        c = Client()
        # can use to '/sw/planet/?filter{id}=%s' % self.planet2.id
        # so returned list result filter.
        # Get by id return dict
        url = '/sw/planet/%s' % self.planet2.id

        # Get Data
        result = c.get(url)
        # get one return planet
        planet_dict = json.loads(result.content)['planet']
        self.assertTrue(isinstance(planet_dict, dict))

        planet =planet_dict
        self.assertEqual(planet['id'], self.planet2.id)
        self.assertEqual(planet['name'], self.planet2.name)
        self.assertEqual(planet['climate'], self.planet2.climate)
        self.assertEqual(planet['terrain'], self.planet2.terrain)
        self.assertEqual(planet['screenings'], self.planet2.get_screenings())

    def test_delete(self):
        """
            Test get planet by id.
        """
        # Delete Yavin IV
        # before delete Total 3 planets
        self.assertEqual(Planet.objects.count(), 3)
        # exists True
        self.assertTrue(Planet.objects.filter(id=self.planet2.id).exists())
        planet = Planet.objects.get(id=self.planet2.id)
        self.assertEqual('Yavin IV', self.planet2.name)
        self.assertEqual(planet.name, self.planet2.name)
        self.assertEqual(planet.climate, self.planet2.climate)
        self.assertEqual(planet.terrain, self.planet2.terrain)

        c = Client()
        # Delete
        url = '/sw/planet/%s' % self.planet2.id

        # Delete
        result = c.delete(url)
        # after delete Total 2 planets
        self.assertEqual(Planet.objects.count(), 2)
        # exists False so self.planet2 deleted
        self.assertFalse(Planet.objects.filter(id=self.planet2.id).exists())
        

        