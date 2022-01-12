from django.shortcuts import render
from datetime import datetime

from django.http import HttpResponse
from django.template import loader

import random

# Create your views here.

def index(request):
    now = datetime.now()
    context = {
        'current_date' : now
    }
    return render(request, 'first/index.html', context)


def select(request):
    context = {}
    return render(request, 'first/select.html', context)

'''
def select(request, year):
    message = '수 하나를 입력해주세요.'
    return HttpResponse(message)
'''

def result(request):
    chosen = int(request.GET['number'])
    
    results = []
    if chosen >=1 and chosen <= 45:
        results.append(chosen)
        
    box = []
    for i in range(1, 46) :
        if chosen != i :
            box.append(i+1)
            
    random.shuffle(box)
    
    while len(results) < 6 :
        results.append(box.pop())      
    
    context = {
        'numbers' : results
    }
    return render(request, 'first/result.html', context)