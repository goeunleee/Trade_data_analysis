from django.shortcuts import render, get_object_or_404, redirect
from .models import Cloud
from datetime import date
from .models import User
from django.http import HttpResponse, JsonResponse
import simplejson as json
import pandas as pd
from .module.trade_predict_model import predict
from django.views.decorators.csrf import csrf_exempt
from .decorators import *

# Create your views here.

@login_message_required
def upload_cloud(request):
    if request.method =="POST":
        subject = request.POST['subject']
        file = request.FILES['file']
        filetype = request.POST['filetype']
        description = request.POST['description']
        ct = User.objects.filter(username=request.user.username).first()
        try:
            Cloud.objects.create(uploadingdate=date.today(),subject=subject,file=file,filetype=filetype,description=description,user=ct)
        except:
            pass 
    cloud = Cloud.objects.all().filter(user=request.user.id)
    return render(request, 'upload_cloud.html',{'cloud':cloud})    

def delete(request, idx):
    cloud = Cloud.objects.get(idx=idx)
    cloud.delete()
    return redirect('/upload_cloud')

@csrf_exempt
def dataTransmit(request):
    try:
        excel_file = request.FILES['file']
        print("엑셀파일:",excel_file)

        predicted_data = predict(excel_file)
        # chart.js 내의 소수점 값에 대한 error를 처리하기 위한 반올림
        for i in range(len(predicted_data)):
            predicted_data[i] = round(predicted_data[i])

        excel_df = pd.read_excel(excel_file, header=1, thousands=',')
        excel_file = excel_df.to_json(orient='columns')
        context_dict = {
            'json_data': excel_file,
            'predicted_data': predicted_data,
            'error': 'no'
        }
        # print(context_dict)
        return JsonResponse(context_dict)

    except Exception as e:
        context_dict = {
            'message': str(e),
            'error': 'yes'
        }
        print(context_dict)
        return JsonResponse(context_dict)

    # return render(request, 'upload_cloud.html', context_dict)
