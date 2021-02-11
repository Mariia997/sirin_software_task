import factory

from alias.models import Alias


class AliasFactory(factory.Factory):
    class Meta:
        model = Alias
