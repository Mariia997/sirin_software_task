from django.db import models
from django.db.models import Q
from django.utils import timezone

from alias.models import Alias


class AliasManager(models.Manager):
    def alias_replace(self, existing_alias, replace_at, new_alias_value):
        """
        Create a new Alias with with alias=new_alias_value and start=replace_at, end=None
        @param existing_alias: existing alias object that will be replaced
        @type existing_alias: Alias
        @param replace_at:
        @type replace_at: datetime
        @param new_alias_value:
        @type new_alias_value:
        @return: new Alias
        @rtype:
        """
        new_alias, _ = Alias.objects.create(
            alias=new_alias_value,
            target=existing_alias.target,
            start=replace_at,
            end=None
        )

        existing_alias.end = replace_at
        existing_alias.save(update_fields=["end"])

        return new_alias

    def get_aliases(self, target, start, to):
        """
        Get aliases with specific start and end
        @param target:
        @type target:str
        @param start:
        @type start: datetime
        @param to:
        @type to: datetime
        @return: Alias object with specific start and end
        @rtype: List[str, Any]
        """
        qs = self.get_queryset()
        alias_objs = qs.filter(Q(end_isnull=True) | Q(end_lte=to), target=target, start_lte=start)

        return alias_objs.values_list("alias", flat=True)


class AliasHistoricalManager(models.Manager):
    def get_queryset(self):
        """
        Get Aliases with specific end
        @return: Aliases with specific end
        @rtype:
        """
        qs = super(AliasHistoricalManager, self).get_queryset()
        qs = qs.filter(end_lt=timezone.now())
        return qs
