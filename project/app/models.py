

from pyexpat import model
from django.db import models
from django.forms import ValidationError
# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(null=True, blank=True)
    dob=models.DateField(auto_now=False, auto_now_add=False)
    country=models.CharField(max_length=40)
    salary=models.IntegerField(null=True,blank=True)

    def __str__(self) -> str:
        return self.name
    def toDict(self):
        return {
            "name":self.name,
            "email":self.email,
            "dob":self.dob,
            "country":self.country
        }
class Products(models.Model):
    name=models.CharField(max_length=50)
    price=models.DecimalField(decimal_places=2,max_digits=7)
    def toDict(self):
        return {
            "name":self.name,
            "price":str(self.price)
        }
    def __str__(self) -> str:
        return self.name
class Rating(models.Model):
    rating=models.DecimalField(decimal_places=1,default=1,max_digits=2)
    user=models.ForeignKey(User, null=True, blank=True,on_delete=models.CASCADE)
    product=models.ForeignKey(Products, null=True, blank=True,on_delete=models.CASCADE)
    def clean(self):
        if(self.rating<1 or self.rating>5):
            raise ValidationError({"rating":"Rating must be between 1 and 5"})
    def toDict(self):
        return {
            "rating":str(self.rating),
            "product":self.product.toDict(),
            "user":self.user.toDict()
        }
    def __str__(self):
        return f"{self.product.name  + self.user.name}"
    
class Test(models.Model):
    x=models.CharField(max_length=27)
    
    class Meta:
        abstract=True
        ordering=['x']
class Texta(Test):
    f=models.CharField(max_length=40)
class Person(models.Model):
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50)
    address=models.CharField(max_length=40)
    age=models.IntegerField()
    def __str__(self) -> str:
        return  f"{self.fname} {self.lname}"
    def toDict(self):
        return {
            "fname":self.fname,
            "lname":self.lname,
            "address":self.address,
            "age":self.age
        }
class Employee(Person):
    employee_id=models.IntegerField()
    department_id=models.IntegerField() 
    def __str__(self):
        return f"{self.fname} {self.lname} (Employee ID: {self.employee_id})"
    def toDict(self):
        return {
            "employee_id":self.employee_id,
            "department_id":self.department_id,
            "person":super().toDict()
            
        }