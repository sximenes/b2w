from django.db import models
import requests

# Create your models here.
class Planet(models.Model):
    name = models.TextField()
    climate = models.TextField(null=True)
    terrain = models.TextField(null=True)

    def get_screenings(self):
        """
            Get screenings(Amount of movies shown) 
            of planet on api https://swapi.co/
            :return: Int - Amount of movies shown get on api returned
               or 0 if not found or many results returned.
        """
        url = 'https://swapi.co/api/planets/?search=%s' % str(self.name)
        r = requests.get(url, timeout=10)
        result = r.json()
        try:
            if result['count']==1:
                return len(result['results'][0]['films'])
        except Exception as e:
            print(str(e))
            return 0
        # Case not found or more one results.
        return 0