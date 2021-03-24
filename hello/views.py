from django.shortcuts import render
from django.http import HttpResponse
import json
import pyodbc

server = "paymentmethodsearchapp-server.database.windows.net"
database = "PaymentStores"
username = "taka19980618"
password = '1mono2DEDENNE'
driver = '{ODBC Driver 17 for SQL Server}'


# Create your views here.
def hello(request):
    # return HttpResponse("Hello, World. You're at the polls index.")

    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    json_data = {"data": []}

    # sql_query = "SELECT * FROM shops ORDER BY abs(" + str(lat) + " - latitude) + abs(" + str(lon) + " - longitude) LIMIT 50;"
    sql_query = "SELECT TOP 50 * FROM paypay_stores1 order by abs(" + lat + \
                "- latitude) + abs(" + lon + " - longitude); "

    with pyodbc.connect(
            'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_query)
            columns = [column[0] for column in cursor.description]
            row = cursor.fetchall()
            for r in row:
                r[4] = str(r[4])
                r[5] = str(r[5])
                r = list(r)
                json_data["data"].append(dict(zip(columns, row)))

    json_str = (json.dumps(json_data, ensure_ascii=False))
    #return render(request, 'polls/index.html', json_data)
    return HttpResponse(json_str)
