from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.fields.fields import DynamicMethodField

from sw.models import Planet

class PlanetSerializer(DynamicModelSerializer):
    screenings = DynamicMethodField()

    def get_screenings(self, obj):
        """
            Get screenings of planet on api https://swapi.co/ 
        """
        return obj.get_screenings()

    class Meta:
        model = Planet
        name = 'planet'
        fields = ('id', 'name', 'climate', 'terrain',
            'screenings')