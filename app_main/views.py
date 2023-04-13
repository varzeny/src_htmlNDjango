from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers

from .apps import NETWORKCONTROLLER

# Create your views here.

from . models import Robot
from . models import Post



def showPage(request):
    if request.method == "POST":
        print(request.POST)
        if request.POST['req'] == 'add_db':
            r = Robot()
            r.name = request.POST['name']
            r.type = request.POST['type']
            r.ip = request.POST['ip']
            r.port = request.POST['port']
            r.note = request.POST['note']
            r.save()
            return redirect('show')
    else:
        robots = Robot.objects.all()
        return render(request, 'app_main/page_main.html', {'robots':robots})

    #render(request, template_name, context=None, content_type=None, status=None, using=None)
    #이 중에서 request 와 template_name 은 필수적으로 필요합니다.
    # request 는 위와 동일하게 써주게 되고,
    # template_name 은 불러오고 싶은 템플릿을 기재해줍니다.
    # 쉽게 생각해서 화면에 html 파일을 띄운다고 생각하면 됩니다.
    # 이 때 context 로 원하는 인자를,
    # 즉 view 에서 사용하던 파이썬 변수를 html 템플릿으로 넘길 수 있습니다.
    # context 는 딕셔너리형으로 사용하며 key 값이 탬플릿에서 사용할 변수이름,
    # value 값이 파이썬 변수가 됩니다.


    #redirect(to, permanent=False, *args, **kwargs)
    # to 에는 어느 URL 로 이동할지를 정하게 됩니다. 
    # 이 때 상대 URL, 절대 URL 모두 가능하며 urls.py 에 name 을 정의하고 이를 많이 사용합니다.
    # 단지 URL로 이동하는 것이기 때문에 render 처럼 context 값을 넘기지는 못합니다.


def dbRead(request):
    pk=request.POST.get('pk')
    record=Robot.objects.get(pk=pk)
    record_json = serializers.serialize('json',[record])

    return JsonResponse({'success':True, 'record':record_json})


def dbRead_forever(request):
    records_json = []
    for pk in NETWORKCONTROLLER.connected:
        record = Robot.objects.get(pk=pk)
        records_json.append(serializers.serialize('json',[record]))

    return JsonResponse({'success':True, 'records':records_json})



def connect(request):
    pk=request.POST.get('pk')
    record=Robot.objects.get(pk=pk)

    try:
        NETWORKCONTROLLER.addConnect(pk,record)
        record.online=True
        record.save()
    except:
        print("add_fail")

    return redirect('show')


def moveUnit(request):
    pk = request.POST.get('pk')
    x = request.POST.get('x')
    y = request.POST.get('y')
    NETWORKCONTROLLER.connected[pk].send_sock(f"gotoPoint {x} {y} 0")
    print("명령 전송됨!")

    return redirect('show')

def sendMsg2Unit(request):
    pk = request.POST.get('pk')
    msg = request.POST.get('msg')

    NETWORKCONTROLLER.connected[pk].send_sock(msg)

    #NETWORKCONTROLLER.connected[pk].send_sock(f"outputOn o1")
    
    print("명령 전송됨!")

    return redirect('show')