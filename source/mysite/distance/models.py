from django.db import models

class Location(models.Model):
    # table for storing location data from rest API
    # values can be null if not found

    location_id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=250, null=True)
    location_lat = models.DecimalField(max_digits=30, decimal_places=20, null=True)
    location_long = models.DecimalField(max_digits=30, decimal_places=20, null=True)
    formatted_location = models.CharField(max_length=250, null=True)

    def indexing(self):
        obj = LocationIndex(
            meta = {'id': self.location_id},
            location = self.location
        )
        obj.save()
        return obj.to_dict(include_meta=True)

    def __str__(self):
        return self.formatted_location



class Distance(models.Model):
    # table for storing origin info, destination info, and calculated distance
    # values can be null if not found

    id = models.AutoField(primary_key=True)

    #origin_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    formatted_origin = models.CharField(max_length=250)
    origin_lat = models.DecimalField(max_digits=30, decimal_places=20, null=True)
    origin_long = models.DecimalField(max_digits=30, decimal_places=20, null=True)

    #estination_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    formatted_destination = models.CharField(max_length=250)
    destination_lat = models.DecimalField(max_digits=30, decimal_places=20, null=True)
    destination_long = models.DecimalField(max_digits=30, decimal_places=20, null=True)

    calculated_distance = models.DecimalField(max_digits=15, decimal_places=2, null=True)

    def __str__(self):
        return self.calculated_distance
