from django.db import models

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=25)
    category_des  = models.CharField(max_length=250)
    category_img  = models.ImageField(upload_to='category_img',null=True,blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name


class Products(models.Model):
    product_name = models.CharField(max_length=25)
    product_cat  = models.ForeignKey(Category,on_delete=models.CASCADE)
    product_des  = models.CharField(max_length=250)
    product_img  = models.ImageField(upload_to='product_img')

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return self.product_name

class Service(models.Model):
    service_name = models.CharField(max_length=250)
    service_product = models.ForeignKey(Products,models.CASCADE)
    service_des = models.CharField(max_length=255)
    service_img = models.ImageField(upload_to='services')

    class Meta:
        verbose_name_plural = "Services"

    def __str__(self):
        return self.service_name