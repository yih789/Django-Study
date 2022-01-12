from django.shortcuts import render, get_object_or_404, redirect
from third.models import Restaurant, Review
from django.core.paginator import Paginator
from third.forms import RestaurantForm, ReviewForm, UpdateRestaurantForm
from django.http import HttpResponseRedirect
from django.db.models import Count, Avg

# Create your views here.
def list(request):
    # 'review'='Review'를 의미 # 'review__point': django규칙
    restaurants = Restaurant.objects.all().annotate(reviews_count=Count('review')).annotate(average_point=Avg('review__point'))
    paginator = Paginator(restaurants, 5)
    
    # 사용자에게 받은 page 파라미터에 맞는 페이지를 전달
    page = request.GET.get('page') ## /third/list/page=1
    items = paginator.get_page(page)
    
    context = {
        'restaurants': items
        
    }
    return render(request, 'third/list.html', context)

def create(request):
    # 사용자가 form에 데이터를 입력할 때
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            new_item = form.save()
        return HttpResponseRedirect('/third/list/')
    # 그냥 create 페이지 접근일 때
    form = RestaurantForm()
    return render(request, 'third/create.html', {'form':form})
        
def update(request):
    if request.method == 'POST' and 'id' in request.POST:
        # item = Restaurant.objects.get(pk=request.POST.get('id'))
        item = get_object_or_404(Restaurant, pk=request.POST.get('id'))
        # '': 사용자가 비밀번호를 입력하지 않으면 빈문자열이 저장된다.
        password = request.POST.get('password', '')
        
        form = UpdateRestaurantForm(request.POST, instance=item)
        
        if form.is_valid() and item.password == password :
            item = form.save()
    elif request.method == 'GET':
        # item = Restaurant.objects.get(pk=request.GET.get('id'))
        item = get_object_or_404(Restaurant, pk=request.GET.get('id'))  
        form = RestaurantForm(instance=item)
        return render(request, 'third/update.html', {'form':form})
    return HttpResponseRedirect('/third/list/')
    
def detail(request, id):
    if 'id' is not None:
        item = get_object_or_404(Restaurant, pk=id)
        reviews = Review.objects.filter(restaurant=item).all()
        return render(request, 'third/detail.html', {'item':item, 'reviews':reviews})
    return HttpResponseRedirect('/third/list/')


def delete(request, id):
    item = get_object_or_404(Restaurant, pk=id)
    if request.method == 'POST' and 'password' in request.POST:
        if item.password == request.POST.get('password') or item.password is None:
            item.delete()
            return redirect('list')
        return redirect('restaurant-detail', id=id)
    return render(request, 'third/delete.html', {'item':item})

# HttpResponseRedirect는 url 주소를 사용하고
# redirect는 url 이름을 사용하기 때문에 변경 발생 시 Redirect가 수정이 용이
def review_create(request, restaurant_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_item = form.save()
        return redirect('restaurant-detail', id=restaurant_id)
    
    item = get_object_or_404(Restaurant, pk=restaurant_id)
    form = ReviewForm(initial={'restaurant': item})
    return render(request, 'third/review_create.html', {'form':form, 'item':item})

def review_delete(request, restaurant_id, review_id):
    item = get_object_or_404(Review, pk=review_id)
    item.delete()
    
    return redirect('restaurant-detail', id=restaurant_id)

def review_list(request):
    # select_related(): join사용
    reviews = Review.objects.all().select_related().order_by('created_at')
    paginator = Paginator(reviews, 10)
    
    page = request.GET.get('page')
    items = paginator.get_page(page)
    
    context = {
        'reviews': items
    }
    return render(request, 'third/review_list.html', context)




