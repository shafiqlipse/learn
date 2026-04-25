from django.db import models

# Create your models here.
class Region(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Zone(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class District(models.Model):
    name = models.CharField(max_length=100)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class School(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class ElectionLevel(models.TextChoices):
    DISTRICT = 'district'
    ZONE = 'zone'
    REGION = 'region'
    NATIONAL = 'national'

class ElectionPositions(models.TextChoices):
    DISTRICT = 'district'
    ZONE = 'zone'
    REGION = 'region'
    NATIONAL = 'national'
    
    
    
class Election(models.Model):
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=20, choices=ElectionLevel.choices)
    position = models.CharField(max_length=20, choices=ElectionPositions.choices)
    district = models.ForeignKey(District, null=True, blank=True, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, null=True, blank=True, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, null=True, blank=True, on_delete=models.CASCADE)

    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Candidate(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    title = models.CharField(max_length=255, choices = [("Headteacher","Headteacher"),("Games Teacher","Games Teacher"),("Director","Director"),])
    gender = models.CharField(max_length=255, choices = [("Male","Male"),("Female","Female"),])
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    
    def __str__(self):
        return f"{self.fname} {self.lname}"
    
    
class Result(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    votes = models.IntegerField()
    election = models.ForeignKey(Election, on_delete=models.CASCADE)

    position = models.IntegerField(null=True, blank=True)
    is_elected = models.BooleanField(default=False)

    result_code = models.CharField(max_length=30, unique=True, blank=True)

    def get_location_label(self):
        level = self.election.level

        if level == 'district' and self.election.district:
            obj = self.election.district

        elif level == 'zone' and self.election.zone:
            obj = self.election.zone

        elif level == 'region' and self.election.region:
            obj = self.election.region

        elif level == 'national':
            return "NAT"

        else:
            return "UNK"

        return f"{obj.name[:3].upper()}{obj.id}"

    def save(self, *args, **kwargs):
        if not self.result_code:
            LEVEL_PREFIX = {
                'district': 'D',
                'zone': 'Z',
                'region': 'R',
                'national': 'N',
            }

            prefix = LEVEL_PREFIX.get(self.election.level, 'X')
            location = self.get_location_label()
            candidate_id = str(self.candidate.id).zfill(5)

            self.result_code = f"{prefix}-{location}-{candidate_id}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.result_code or f"Result {self.id}"

    class Meta:
        unique_together = ('candidate', 'election')