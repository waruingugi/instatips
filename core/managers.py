from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Max


class CustomManager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        """
        Default model managers do not call signals or custom methods,
        So overide manager with custom manager
        ... OTHER BTW'S ...
        for some reason python 3 return code snippet does not work:
        >> return super().bulk_create(objs,**kwargs)
        so use python 2 return code snippet:
        >> return super(models.Manager,self).bulk_create(objs,**kwargs)
        """
        for obj in objs:
            obj.save()
        return objs

    def get_max_league_id(self):
        """
        Get the latest league id e.g if league id's are 1,2,3
        then return 3 as the highest league id.
        """
        result = []
        try:
            self.model._meta.get_field('league_id')
            result = self.model.objects.all().aggregate(Max('league_id'))
        except FieldDoesNotExist:  # noqa
            raise ValidationError(
                '{0} has no field named league_id'.format(self.model)
            )
        return result
