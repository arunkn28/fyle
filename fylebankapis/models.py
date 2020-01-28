from django.db import models


class Banks(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'banks'


class Branches(models.Model):
    ifsc = models.CharField(max_length=11, primary_key=True)
    bank_id = models.BigIntegerField()
    branch = models.CharField(max_length=74)
    address = models.CharField(max_length=195)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=26)

    class Meta:
        db_table = 'branches'


class BankBranches(models.Model):
    ifsc = models.CharField(max_length=11, primary_key=True)
    bank_id = models.ForeignKey(Branches, on_delete=models.DO_NOTHING)
    branch = models.CharField(max_length=74)
    address = models.CharField(max_length=195)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=26)

    class Meta:
        managed = False
        db_table = 'bank_branches'
