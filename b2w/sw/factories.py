import factory
from sw.models import Planet


class PlanetFactory(factory.Factory):
    class Meta:
        model = Planet

    name = factory.Sequence(lambda n: 'Planeta%s' % n)
    climate = factory.Sequence(lambda n: 'climate%s' % n)
    terrain = factory.Sequence(lambda n: 'Terrain%s' % n)