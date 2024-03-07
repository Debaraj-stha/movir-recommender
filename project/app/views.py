from django.db import connection
from django.shortcuts import render,HttpResponse
from .models import *
from django.db.models import Count,Avg,Q

# Create your views here.
def load_index(request):
    return HttpResponse("index file")
def getAverageProductRating():
    users=User.objects.annotate(num_products_rated=Count('rating__product', distinct=True)).filter(num_products_rated__gte=2)
    products=Products.objects.filter(rating__user__in=users)
    avg_rating=Rating.objects.filter(product__in=products).values('product').annotate(avg_rating=Avg('rating')).order_by('-avg_rating')
    print(users)
    print(products)
    for avg_rate in avg_rating:
        print(avg_rate)
def getRatingRateByUser(userId):
    user=User.objects.filter(id=userId).first()
    products=Rating.objects.filter(user=user)
    print(f"Product rate by user  {user.name}")
    for product in products:
        print(product)
def getUserWhoHaveRatedProduct():
    rating_user=Rating.objects.values('user').distinct()
    users=User.objects.filter(id__in=rating_user)
    print(users)
    print(rating_user)
    
# getAverageProductRating()
# getRatingRateByUser(1)
# getUserWhoHaveRatedProduct()
def getProductAverageRating():
    rating=Products.objects.annotate(avg_rating=Avg('rating__rating')).order_by('-avg_rating')[:5]
    for rate in rating:
        print(round(rate.avg_rating,1))
getProductAverageRating()
def andQuery():
    user=User.objects.filter(Q(name='xyz') & Q(country='nepal'))
    print([u.toDict() for u in user])
def orQuery():
    user=User.objects.filter(Q(name='xyz') | Q(country='nepal'))
    print([u.toDict() for u in user])
def excludeQuery():
    user=User.objects.exclude(email__isnull=True)
    print([u.toDict() for u in user])
# orQuery()
def notQuery():
    print("not query")
    user=User.objects.filter(~Q(name='xyz'))
    print([u.toDict() for u in user])
def raquoQuery():
    cur=connection.cursor()
    cur.execute("select * from app_User")
    p=cur.fetchall()
    print(p)