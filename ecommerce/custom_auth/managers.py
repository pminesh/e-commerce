from django.contrib.auth.models import UserManager
from django.db.models import QuerySet


class ApplicationUserQuerySet(QuerySet):
    def with_statistic(self):
        print("with_statistic")
        return self.with_filters_amount()

    def with_filters_amount(self):
        print("with_filters_amount")
        return self.annotate(
            filter_amount=1,
        )


class ApplicationUserManager(UserManager.from_queryset(ApplicationUserQuerySet)):
    use_in_migrations = True

    @classmethod
    def normalize_email(cls, email):
        if not email:
            return None
        return super().normalize_email(email)

    def get_by_natural_key(self, value):
        return self.get(**{'%s__iexact' % self.model.USERNAME_FIELD: value})
