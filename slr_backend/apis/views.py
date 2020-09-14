from django.shortcuts import render

# Create your views here.
from boto3.dynamodb.conditions import Key, Attr
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
import boto3
import json
import logging
from json import JSONEncoder
import datetime
from statistics import mean
import pytz
from django.views.generic import View
from collections import OrderedDict
tz=pytz.timezone(settings.TIME_ZONE)
logger = logging.getLogger(__name__)
session = boto3.Session(
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)
dynamodb = session.resource('dynamodb', region_name='us-west-2')


class TimeLevels:
    def __init__(self):
        self.now = datetime.datetime.now(tz=tz)
        self.curr_year = self.now.year
        if self.now.month < 10:
            self.curr_month = int(str(self.curr_year) + "0" + str(self.now.month))
        else:
            self.curr_month = int(str(self.curr_year) + str(self.now.month))
        if self.now.day < 10:
            self.curr_day = int(str(self.curr_month) + "0" + str(self.now.day))
        else:
            self.curr_day = int(str(self.curr_month) + str(self.now.day))
        if self.now.hour < 10:
            self.curr_hour = int(str(self.curr_day) + "0" + str(self.now.hour))
        else:
            self.curr_hour = int(str(self.curr_day) + str(self.now.hour))

        if datetime.date.today().isocalendar()[1] < 10:
            self.curr_week = int(str(self.curr_year) + "0" + str(datetime.date.today().isocalendar()[1]))
        else:
            self.curr_week = int(str(self.curr_year) + str(datetime.date.today().isocalendar()[1]))



class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def IsUpdateRequired(table, deviceId, granularity,curr_time):
    if granularity == "hour":
        curr=curr_time.curr_hour
        table_name = table + "_hourly"
    elif granularity == "day":
        curr=curr_time.curr_day
        table_name = table + "_daily"
    else:
        curr=curr_time.curr_week
        table_name = table + "_weekly"
    data_table = dynamodb.Table(table_name)
    data_table_og = dynamodb.Table(table+"_data")
    #print(curr)
    if granularity == "hour":
        response=data_table.get_item(
            Key={
                'hour': curr,
                'deviceId': deviceId
            }
        )
    elif granularity == "day":
        response = data_table.get_item(
            Key={
                'day': curr,
                'deviceId': deviceId
            }
        )
    else:
        response = data_table.get_item(
            Key={
                'week': curr,
                'deviceId': deviceId
            }
        )
    if 'Item' in response:
        #print("Hourly table not updated")

        response_check = data_table_og.scan(
            FilterExpression=Attr(granularity).eq(curr) & Attr('deviceId').eq(deviceId)
        )
        sum_curr_c = 0
        items = response_check['Items']
        # print(items)
        for i in range(len(items)):
            sum_curr_c += items[i]['deviceValue']
        if response['Item']['deviceValue'] != round(sum_curr_c / len(items),2):
            data_table.update_item(
                Key={
                    granularity: curr,
                    'deviceId': deviceId
                },
                UpdateExpression='SET deviceValue = :val1',
                ExpressionAttributeValues={
                    ':val1': round(sum_curr_c / len(items),2)
                }
            )
        return False
    else:
        return 'Item' not in response


def updateData(table,deviceId, granularity,curr_time):
    data_table=table+"_data"
    if granularity == "hour":
        curr=curr_time.curr_hour
        granular_table=table+"_hourly"
    elif granularity == "day":
        curr=curr_time.curr_day
        granular_table = table+"_daily"
    else:
        curr=curr_time.curr_week
        granular_table = table+"_weekly"
    curr_c=curr
    data_table_og = dynamodb.Table(data_table)

    data_table_granularly = dynamodb.Table(granular_table)

    response_size = data_table_granularly.scan(
        FilterExpression=Attr(granularity).gt(0) & Attr('deviceId').eq(deviceId)
    )

    if len(response_size['Items']) == 0:
        empty_granularly = True
    else:
        empty_granularly = False

    while True and not empty_granularly:
        if granularity == "hour":
            response = data_table_granularly.get_item(
                Key={
                    'hour': curr_c,
                    'deviceId': deviceId
                }
            )
        elif granularity == "day":
            response = data_table_granularly.get_item(
                Key={
                    'day': curr_c,
                    'deviceId': deviceId
                }
            )
        else:
            response = data_table_granularly.get_item(
                Key={
                    'week': curr_c,
                    'deviceId': deviceId
                }
            )
        if 'Item' in response:
            break
        if curr_c%100==0:
            if granularity=='hour':
                curr_c-=77
            elif granularity=='day':
                curr_c-=69
            elif granularity=='week':
                curr-=47
        curr_c -= 1
    after_items=[]
    if not empty_granularly:
        item = response['Item']
        response_check = data_table_og.scan(
            FilterExpression=Attr(granularity).eq(curr_c) & Attr('deviceId').eq(deviceId)
        )
        sum_curr_c = 0
        items = response_check['Items']
        for i in range(len(items)):
            sum_curr_c += items[i]['deviceValue']
        if not empty_granularly and item['deviceValue'] != round(sum_curr_c / len(items),2):
            data_table_granularly.update_item(
                Key={
                    granularity: curr_c,
                    'deviceId': deviceId
                },
                UpdateExpression='SET deviceValue = :val1',
                ExpressionAttributeValues={
                    ':val1': round(sum_curr_c / len(items),2)
                }
            )
        response = data_table_og.scan(
            FilterExpression=Attr(granularity).gt(curr_c) & Attr('deviceId').eq(deviceId)
        )
        after_items = response['Items']

    else:
        curr_c = 0
        response = data_table_og.scan(
            FilterExpression=Attr('deviceId').eq(deviceId)
        )
        after_items = response['Items']
    if len(after_items)>0:
        sum1 = after_items[0]['deviceValue']
        count1=1
        avg_calc={}
        for i in range(len(after_items)):
            if after_items[i][granularity] not in avg_calc:
                avg_calc[after_items[i][granularity]]={}
                avg_calc[after_items[i][granularity]]['deviceValue']=[]
                avg_calc[after_items[i][granularity]]['deviceValue'].append(after_items[i]['deviceValue'])
                avg_calc[after_items[i][granularity]]['deviceParameter']=after_items[i]['deviceParameter']
                avg_calc[after_items[i][granularity]]['deviceId']=after_items[i]['deviceId']
                avg_calc[after_items[i][granularity]]['year']=after_items[i]['year']
                avg_calc[after_items[i][granularity]]['month']=after_items[i]['month']
                if granularity=='hour':
                    avg_calc[after_items[i][granularity]]['day']=after_items[i]['day']
                    avg_calc[after_items[i][granularity]]['week']=after_items[i]['week']
                elif granularity=='day':
                    avg_calc[after_items[i][granularity]]['week'] = after_items[i]['week']
            else:
                avg_calc[after_items[i][granularity]]['deviceValue'].append(after_items[i]['deviceValue'])
        for i in avg_calc:
            if granularity=="hour":
                data_table_granularly.put_item(
                    Item={
                        'hour': i,
                        'deviceValue': round(mean(avg_calc[i]['deviceValue']),2),
                        'deviceParameter': avg_calc[i]['deviceParameter'],
                        'deviceId': avg_calc[i]['deviceId'],
                        'year': avg_calc[i]['year'],
                        'month': avg_calc[i]['month'],
                        'day': avg_calc[i]['day'],
                        'week': avg_calc[i]['week'],
                    }

                )
            elif granularity=="day":
                data_table_granularly.put_item(
                Item = {
                    'day': i,
                    'deviceValue': round(mean(avg_calc[i]['deviceValue']),2),
                    'deviceParameter': avg_calc[i]['deviceParameter'],
                    'deviceId': avg_calc[i]['deviceId'],
                    'year': avg_calc[i]['year'],
                    'month': avg_calc[i]['month'],
                    'week': avg_calc[i]['week']
                }

                )
            else:
                data_table_granularly.put_item(
                Item = {
                    'week': i,
                    'deviceValue': round(mean(avg_calc[i]['deviceValue']),2),
                    'deviceParameter': avg_calc[i]['deviceParameter'],
                    'deviceId': avg_calc[i]['deviceId'],
                    'year': avg_calc[i]['year'],
                    'month': avg_calc[i]['month']
                }

                )

def subtractDays(curr_day, numberOfDays):
    return int((datetime.datetime.strptime(curr_day, '%Y%m%d') - datetime.timedelta(days=numberOfDays)).strftime(
        "%Y%m%d"))


def subtractHours(curr_hour, numberOfHours):
    return int((datetime.datetime.strptime(curr_hour, '%Y%m%d%H') - datetime.timedelta(hours=numberOfHours)).strftime("%Y%m%d%H"))


def subtractWeeks(curr_week, numberOfWeeks):
    return int((datetime.datetime.strptime(curr_week + '-1', "%Y%W-%w") - datetime.timedelta(weeks=numberOfWeeks)).strftime(
        "%Y%W"))


def calculateGranularData(request,table,deviceId,granularity,curr_time):
    if IsUpdateRequired(table,deviceId,granularity,curr_time):
        updateData(table,deviceId,granularity,curr_time)
    if granularity=="hour":
        table_name = table + "_hourly"
        subnum = 24
        curr = subtractHours(str(curr_time.curr_hour), subnum)

    elif granularity == "day":
        table_name = table + "_daily"
        subnum = 30
        curr = subtractDays(str(curr_time.curr_day), subnum)

    else:
        table_name = table + "_weekly"
        subnum = 16
        curr = subtractWeeks(str(curr_time.curr_week), subnum)
    data_table = dynamodb.Table(table_name)

    response = data_table.scan(
        FilterExpression = Attr(granularity).gt(curr) & Attr('deviceId').eq(deviceId)
    )
    ans={}
    for item in response['Items']:
        for key in item:
            item[key]=str(item[key])
        ans[int(item[granularity])] = item
    return sorted(ans),ans


def getGranularData(request,table,deviceId,granularity,curr_time):
    return HttpResponse(json.dumps(calculateGranularData(request,table,deviceId,granularity,curr_time), cls=MyEncoder))


def convertDataForChart(request,table, deviceId, granularity, curr_time):
    sorted_keys, ans = calculateGranularData(request, table, deviceId, granularity,curr_time)
    data = {}
    data['labels'] = []
    data['values'] = []
    if granularity=='hour':
        subnum=20
    elif granularity=='day':
        subnum=20
    else:
        subnum=16
    #print(curr_time.curr_hour)
    for sub in range(subnum):
        if granularity == 'hour':
            item = subtractHours(str(curr_time.curr_hour), sub)
            data['labels'].append((datetime.datetime.strptime(str(item), '%Y%m%d%H').strftime('%H:%M')))
        elif granularity == 'day':
            item = subtractDays(str(curr_time.curr_day), sub)
            data['labels'].append((datetime.datetime.strptime(str(item), '%Y%m%d').strftime('%m/%d')))
        else:
            item = subtractWeeks(str(curr_time.curr_week), sub)
            data['labels'].append(datetime.datetime.strptime(str(int(item)-1) + '-1', "%Y%W-%w").strftime('%m/%d'))



        if item in ans:
            val = ans[item]['deviceValue']
        else:
            val = 0
        data['values'].append(val)
    data['values'].reverse()
    data['labels'].reverse()
    return data


def getRawData(request,table,deviceId):
    curr_time = TimeLevels()
    table_name=table+"_data"
    data_table = dynamodb.Table(table_name)
    response = data_table.scan(
        FilterExpression=Attr('deviceId').eq(deviceId)
    )
    ans = {}
    for item in response['Items']:
        print(item)
        for key in item:
            item[key] = str(item[key])
        ans[str(item['timestamp'])] = item
    return HttpResponse(json.dumps(ans, cls=MyEncoder))

def getCurrentValues(request,table,deviceId):
    curr_time = TimeLevels()
    table_name = table + "_data"
    data_table = dynamodb.Table(table_name)
    response = data_table.scan(
        FilterExpression=Attr('deviceId').eq(deviceId) & Attr('hour').eq(curr_time.curr_hour)
    )
    if len(response['Items']) > 0:
        ans = {}
        for item in response['Items']:
            timestamp = datetime.datetime.timestamp(datetime.datetime.strptime(item['timestamp'], '%Y-%m-%d %H:%M:%S'))
            ans[timestamp]=item['deviceValue']
        sortedbykey = {k: v for k, v in sorted(ans.items(), key=lambda item: item[0], reverse=True)}
        #sortedbykey = OrderedDict(sorted(ans.items(), reverse=True))
        print(sortedbykey)
        return {str(datetime.datetime.fromtimestamp(list(sortedbykey.keys())[0])):sortedbykey[list(sortedbykey.keys())[0]]}
    else:
        return "No Values"



def displayDashboard(request):
    #inflow_data= getRawData(request,'inflow', settings.SENSORS[site]['inflow'])
    curr_time = TimeLevels()
    alldata = {}
    for site in settings.SENSORS:
        #print(site)
        alldata[site] = {}
        for sensor in settings.SENSORS[site]:
            #print(sensor)

            alldata[site][settings.SENSORS[site][sensor]] = {}
            alldata[site][settings.SENSORS[site][sensor]]['curr_values']=getCurrentValues(request,sensor,settings.SENSORS[site][sensor])
            for i in range(len(settings.GRAIN)):
                #print(settings.GRAIN[i])
                alldata[site][settings.SENSORS[site][sensor]][settings.GRAIN[i]] = convertDataForChart(request, sensor, settings.SENSORS[site][sensor], settings.GRAIN[i],curr_time)


    # inflow_hourly = convertDataForChart(request,'inflow', settings.SENSORS[site]['inflow'], settings.GRAIN[0])
    # inflow_daily = convertDataForChart(request,'inflow', settings.SENSORS[site]['inflow'], settings.GRAIN[1])
    # inflow_weekly = convertDataForChart(request,'inflow', settings.SENSORS[site]['inflow'], settings.GRAIN[2])
    # #outflow_data = getRawData(request, 'outflow', settings.SENSORS[site]['outflow'])
    # outflow_hourly = convertDataForChart(request, 'outflow', settings.SENSORS[site]['outflow'], settings.GRAIN[0])
    # outflow_daily = convertDataForChart(request, 'outflow', settings.SENSORS[site]['outflow'], settings.GRAIN[1])
    # outflow_weekly = convertDataForChart(request, 'outflow', settings.SENSORS[site]['outflow'], settings.GRAIN[2])
    # #turbidity_data = getRawData(request, 'turbidity', settings.SENSORS[site]['turbidity'])
    # turbidity_hourly = convertDataForChart(request, 'turbidity', settings.SENSORS[site]['turbidity'], settings.GRAIN[0])
    # turbidity_daily = convertDataForChart(request, 'turbidity', settings.SENSORS[site]['turbidity'], settings.GRAIN[1])
    # turbidity_weekly = convertDataForChart(request, 'turbidity', settings.SENSORS[site]['turbidity'], settings.GRAIN[2])
    # #oxygen_data = getRawData(request, 'dissolvedoxygen', settings.SENSORS[site]['dissolvedoxygen'])
    # oxygen_hourly = convertDataForChart(request, 'dissolvedoxygen', settings.SENSORS[site]['dissolvedoxygen'], settings.GRAIN[0])
    # oxygen_daily = convertDataForChart(request, 'dissolvedoxygen', settings.SENSORS[site]['dissolvedoxygen'], settings.GRAIN[1])
    # oxygen_weekly = convertDataForChart(request, 'dissolvedoxygen', settings.SENSORS[site]['dissolvedoxygen'], settings.GRAIN[2])
    # data ={'inflow_hourly':inflow_hourly, 'inflow_daily': inflow_daily, 'inflow_weekly': inflow_weekly, 'outflow_hourly':outflow_hourly, 'outflow_daily':outflow_daily, 'outflow_weekly':outflow_weekly, 'turbidity_hourly': turbidity_hourly, 'turbidity_daily': turbidity_daily, 'turbidity_weekly': turbidity_weekly, 'oxygen_hourly': oxygen_hourly, 'oxygen_daily': oxygen_daily, 'oxygen_weekly': oxygen_weekly}

    #return render(request, 'dashboard.html', {'data': alldata}, status=200)
    print(alldata)
    return JsonResponse(alldata)



class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard.html', {})
