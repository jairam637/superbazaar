from bazaarapp.models import Items
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import csv


class Command(BaseCommand):
    help = 'Inserts data to database from csv file'

    def handle(self, *args, **options):
        with open("bazaarapp/static/csv/items.csv", "r") as csvfile:
            readfile = csv.DictReader(csvfile)
            Items.objects.all().delete()

            for row in readfile:
                    a = Items()
                    a.item_id = row['item_id']
                    a.item_name = row['name']
                    a.item_category = row['category']
                    a.item_brand = row['brand']
                    a.item_price = row['price']
                    a.save()


