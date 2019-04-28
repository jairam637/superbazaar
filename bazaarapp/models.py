from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
import datetime


class MyRegistrationForm(UserCreationForm):
    email = forms.CharField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super(MyRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class UserTable(models.Model):
    user_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    mobile = models.CharField(max_length=15, unique=True, default=None)
    address = models.CharField(max_length=100, default=None)
    state = models.CharField(max_length=30, default=None)
    pincode = models.IntegerField(default=None)
    country = models.CharField(max_length=20, default=None)

    class Meta:
        db_table = 'UserTable'


class Items(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=200, default=None)
    item_category = models.CharField(max_length=200, default=None)
    item_brand = models.CharField(max_length=200, default=None)
    item_price = models.FloatField(default=None)

    class Meta:
        db_table = 'Items'


class Transaction(models.Model):
    trans_id = models.AutoField(primary_key=True)
    date = models.DateField(default=None)
    time = models.TimeField(default=None)
    total_amount = models.FloatField(default=None)

    class Meta:
        db_table = 'Transaction'


class TransactionItem(models.Model):
    trans_item_id = models.ForeignKey(Transaction)
    item_id = models.ForeignKey(Items)
    Number_of_items = models.IntegerField(default=None)

    class Meta:
        db_table = 'Transaction_item'


def get_catagories():
    queryset = Items.objects.all().values('item_category').distinct()
    aggregate = [i['item_category'] for i in list(queryset)]
    aggregate_json = {'item_category': aggregate}
    return aggregate_json


def get_brands(catagory):
    queryset = Items.objects.all().filter(item_category=catagory) \
        .values('item_brand').distinct()
    aggregate = [i['item_brand'] for i in list(queryset)]
    aggregate_json = {'item_brand': aggregate}
    return aggregate_json


def get_item(catagory, brand):
    queryset = list(Items.objects.filter(item_category__exact=catagory) \
                    .filter(item_brand=brand) \
                    .values('item_name', 'item_price'))

    catagories = {i['item_name']: i['item_price'] for i in list(queryset)}
    return catagories


def store_transaction(data):
    transaction = Transaction()
    transaction.date = datetime.date.today()
    transaction.time = datetime.datetime.now().time()
    transaction.total_amount = 0
    # user_id = list(User.objects.filter(username= username).values('id'))[0]["id"]
    # transaction.cust_id = user_id
    transaction.save()
    total = 0
    for each in data.values():
        try:
            total += int(each[4])
            transaction_item = TransactionItem()
            item_id = Items.objects.filter(item_category=each[0])\
                                   .filter(item_brand=each[1]) \
                                   .filter(item_name=each[2]).get()
            transaction_item.trans_item_id = transaction
            transaction_item.item_id = item_id
            transaction_item.Number_of_items = int(each[3])
            transaction_item.save()
        except IndexError:
            print("---------------------caugt Exc")

    transaction.total = total
    transaction.save()

    return {"id": transaction.trans_id}
# def get_item_sold():
#     itemlist = Items.objects.values(id)
#     queryset = list(Transaction_item.objects.all().filter(item_id=itemlist))
