from django.contrib.auth.models import UserManager
from django.db.models import QuerySet


class ApplicationUserQuerySet(QuerySet):
    def with_statistic(self):
        print("data")
        return self.with_filters_amount()

    def with_filters_amount(self):
        return self.annotate(
            filter_amount=1,
        )


class CartManager(UserManager.from_queryset(ApplicationUserQuerySet)):
    use_in_migrations = True
