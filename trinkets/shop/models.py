from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    desc = models.TextField(verbose_name='description', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse(
            'shop:product_list_by_category', args=[self.slug]
        )

    def __str__(self):
        return self.name

class Inventory(models.Model):
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.quantity)
    
class Discount(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(verbose_name='description')
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='discount in percentage'
    )
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    
class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )
    quantity = models.OneToOneField(
       Inventory,
       related_name='product_quantity',
       on_delete=models.CASCADE,
       null=True
    )
    discount = models.ForeignKey(
        Discount,
        related_name='product_discounts',
        on_delete=models.CASCADE,
        null=True
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(
        upload_to='products/%Y/%m/%d',
        blank=True
    )
    desc = models.TextField(blank=True, verbose_name='description')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
        ]
    
    def get_absolute_url(self):
        return reverse(
            'shop:product_detail', args=[self.id, self.slug]
        )
    
    def __str__(self):
        return self.name
    

