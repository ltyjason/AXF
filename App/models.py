import hashlib

from django.db import models


class Main(models.Model):
    img = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
    trackid = models.IntegerField(default=1)

    class Meta:
        abstract = True


class MainWheel(Main):

    class Meta:
        db_table = 'axf_wheel'


class MainNav(Main):

    class Meta:
        db_table = 'axf_nav'


class MainMustBuy(Main):

    class Meta:
        db_table = 'axf_mustbuy'


class MainShop(Main):

    class Meta:
        db_table = 'axf_shop'


class MainMainShow(Main):

    categoryid = models.IntegerField(default=1)

    brandname = models.CharField(max_length=32)

    img1 = models.CharField(max_length=200)

    childcid1 = models.IntegerField(default=1)

    productid1 = models.IntegerField(default=1)

    longname1 = models.CharField(max_length=200)

    price1 = models.FloatField(default=0)

    marketprice1 = models.FloatField(default=0)

    img2 = models.CharField(max_length=200)

    childcid2 = models.IntegerField(default=1)

    productid2 = models.IntegerField(default=1)

    longname2 = models.CharField(max_length=200)

    price2 = models.FloatField(default=0)

    marketprice2 = models.FloatField(default=0)

    img3 = models.CharField(max_length=200)

    childcid3 = models.IntegerField(default=1)

    productid3 = models.IntegerField(default=1)

    longname3 = models.CharField(max_length=200)

    price3 = models.FloatField(default=0)

    marketprice3 = models.FloatField(default=0)

    class Meta:
        db_table = 'axf_mainshow'


class FoodType(models.Model):

    typeid = models.IntegerField(default=1)

    typename = models.CharField(max_length=16)

    childtypenames = models.CharField(max_length=200)

    typesort = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_foodtypes'


class Goods(models.Model):

    productid = models.IntegerField(default=1)

    productimg = models.CharField(max_length=200)

    productname = models.CharField(max_length=128)

    productlongname = models.CharField(max_length=200)

    isxf = models.BooleanField(default=False)

    pmdesc = models.BooleanField(default=False)

    specifics = models.CharField(max_length=32)

    price = models.FloatField(default=0)

    marketprice = models.FloatField(default=1)

    categoryid = models.IntegerField(default=1)

    childcid = models.IntegerField(default=1)

    childcidname = models.CharField(max_length=128)

    dealerid = models.IntegerField(default=1)

    storenums = models.IntegerField(default=1)

    productnum = models.IntegerField(default=1)


    class Meta:
        db_table = 'axf_goods'


class UserModel(models.Model):

    u_name = models.CharField(max_length=16, unique=True)

    password = models.CharField(max_length=256)

    u_email = models.CharField(max_length=32, unique=True)

    u_icon = models.ImageField(upload_to='%Y/%m/%d/icons')

    is_delete = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)

    # 对数据生成sha的hash
    def generate_hash(self, u_password):
        sha = hashlib.sha512()
        sha.update(u_password.encode('utf-8'))
        return sha.hexdigest()

    # 通过指定方式来设置密码
    def set_password(self, u_password):
        self.password = self.generate_hash(u_password)

    # 提供密码验证方式
    def check_password(self, u_password):
        return self.password == self.generate_hash(u_password)


class CarModel(models.Model):

    c_user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    c_goods = models.ForeignKey(Goods, on_delete=models.CASCADE)

    c_goods_num = models.IntegerField(default=1)

    c_goods_select = models.BooleanField(default=True)
