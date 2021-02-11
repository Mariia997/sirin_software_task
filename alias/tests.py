from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from alias.factory import AliasFactory
from alias.models import Alias


class AliasManagerTest(TestCase):
    def setUp(self) -> None:
        self.existing_alias = AliasFactory()
        self.new_alias_value = "new_alias_value"

    def test_alias_replace_old_alias_after_replace(self):
        replace_at = timezone.now()

        _ = Alias.objects.alias_replace(
            existing_alias=self.existing_alias,
            replace_at=replace_at,
            new_alias_value=self.new_alias_value

        )

        self.existing_alias.refresh_from_db()
        self.assertEqual(self.existing_alias.end, replace_at)

    def test_alias_replace_new_alias(self):
            replace_at = timezone.now()

            new_alias = Alias.objects.alias_replace(
                existind_alias=self.existing_alias,
                replace_at=replace_at,
                new_alias_value=self.new_alias_value
            )

            self.assertEqual(new_alias.alias, self.new_alias_value)
            self.assertIsNone(new_alias.end)


class HistoricalAliassManagerTest(TestCase):
    def test_historical_end_is_not_null(self):
        exist_null = Alias.historical_objs.filter(end__isnull=True).exists()
        self.assertFalse(exist_null)


class AliasTest(TestCase):
    def test_overlap_success(self):
        active_alias = Alias.objects.create()

        new_alias, created = Alias.objects.create(
            alias=active_alias.alias,
            target=active_alias.target,
            end="other",
            start='other'
        )

        self.assertTrue(created)

    def test_overlap_fail(self):
        active_alias = Alias.objects.create()
        new_alias = active_alias
        new_alias.pk = None

        with self.assertRaises(ValidationError):
            new_alias.save()
