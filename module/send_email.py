# -*- coding: utf-8 -*-
# chmod -R 755 /hive/bin/hive
import os
import re
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import xlwt
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import numpy as np
import pandas as pd
import datetime
import sys
from scipy.interpolate import spline
import numpy

#reload(sys)
#sys.setdefaultencoding('utf-8')

#run_job_data_path = sys.argv[1]
#run_job_date10 = sys.argv[2]
#run_job_date8 = run_job_date10.replace('-','')

now=datetime.datetime.now()
today=now.strftime('%Y%m%d')
delta_week=datetime.timedelta(days=7)
delta_day=datetime.timedelta(days=1)
new_dt=now-delta_week
new_dt1=now-delta_day
#new_dt2 = datetime.datetime.strptime(run_job_date10, '%Y-%m-%d')
new_dt1 = new_dt1.strftime('%Y%m%d')

dt_mark=[]
for i in range(7,0,-1):
	delta=datetime.timedelta(days=i)
	new_date=now-delta
	new_date1=new_date.strftime('%m%d')
	dt_mark.append(new_date1)
T7=now-delta_day*7
T6=now-delta_day*6
T5=now-delta_day*5
T4=now-delta_day*4
T3=now-delta_day*3
T2=now-delta_day*2
T1=now-delta_day*1
T7=T7.strftime('%Y%m%d')
T6=T6.strftime('%Y%m%d')
T5=T5.strftime('%Y%m%d')
T4=T4.strftime('%Y%m%d')
T3=T3.strftime('%Y%m%d')
T2=T2.strftime('%Y%m%d')
T1=T1.strftime('%Y%m%d')

data1=os.popen("""hive -e "
select 
sourcetype,risk_type,description,code,user_num,pin_hit_rate,pin_hit_rate_2,pin_hit_rate_7
,max_tr_hit_rate,order_num,order_hit_rate,order_hit_rate_2,order_hit_rate_7
,max_or_hit_rate
from rt_test.cyx_stragety_sourcetype_orderid_6
where dt = '20191217' and risk_type is not null and description is not null 
order by user_num desc;"
""").readlines()

new_data1=[]
for i in data1:
    read=i.split('\t')
    new_data1_1=[]
    for j in range(len(read)):
        a=read[j]
        if j in [0,1,2,3]:
            b = a
        elif j in [4,9]:
            if a == 'NULL':
                b = 0
            else:
                b = int(a)
        else:
            if a == 'NULL':
                b = 0
            else:
                b = str(round(float(a) * 100, 4)) + '%'
                if b == '0.0%':
                    b = '0.000%'
                elif b == '-0.0%':
                    b = '-0.000%'
                else:
                    pass
        new_data1_1.append(b)
    new_data1.append(new_data1_1)

lab_mark1=[u'场景',u'风险类型',u'策略描述',u'决策状态',u'触发pin数',u'pin触发率',u'pin触发率1天波动',u'pin触发率7天波动',u'pin近30天最大触发率',u'触发订单数',u'订单触发率',u'订单触发率1天波动',u'订单触发率7天波动',u'订单近30天最大触发率']
out_dt1=pd.DataFrame(new_data1,columns=lab_mark1)

#生成表，并设置格式
def gettable1(row,col,file): #row指的是行，col指的是列
	column = file.columns
	ind = file.index
	table = ""
	for i in range(row):
		table+="<tr>"
		for j in range(col):
			if i==0:
				table += "<td style=\"WHITE-SPACE: nowrap;text-align:center;font-weight:bolder;color:white;background-color:rgb(100,149,237)\">%s</td>" % str(column[j])
			elif i>0 and j in [2]:
				table += "<td style=\"width:50%"+";text-align:center;font-weight:bolder;background-color:#FFFFFF\">%s</td>" % file.at[ind[i-1], column[j]]		
			# elif i>0 and j in [6]:
				# table += "<td style=\"WHITE-SPACE: nowrap;text-align:center;background-color:#FFFFFF\">%.2f%%</td>" % file.at[ind[i-1], column[j]]	
			else:
				table += "<td style=\"WHITE-SPACE: nowrap;text-align:center;font-weight:bolder;background-color:#FFFFFF\">%s</td>" % file.at[ind[i-1], column[j]]		
		table += "</tr>\n"
	return table  

# 表格属性设置
header = "<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd\">"
header += "<html>"
header += "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />"
header += "<title>bank</title>"
header += "<style type='text/css' rel='stylesheet'>"
header += "table{"
header += "border-collapse:collapse;"
header += "border-left:1px solid #000000;"
header += "border-spacing:0;"
header += "border:1px solid #000000;"
header += "outline:0px solid #000000;"
header += "padding:1.5px;"
header += "vertical-align:right;"
header += "margin-bottom:10px;"
header += "font-size:12px;"
header += "background-color:#E8B388;"
header += "height:15px;"
header += "}"
header += "table th{"
header += "text-align:left;"
header += "background-color:#88ACEC;"
header += "font-weight:bolder;"
header += "color:#FFAA00;"
header += "margin-bottom:-3px;"
header += "padding:2px 10px;"
header += "text-align:center;"
header += "border-bottom:1px solid #000000;"
header += "border-right:1px solid #000000;"
header += "color:#000000;"
header += "}"
header += "table tr td{"
header += "margin-bottom:-3px;"
header += "padding:2px 10px;"
header += "border-bottom:1px solid #000000;"
header += "border-right:1px solid #000000;"
header += "color:#000000;"
header += "}"
header += ".lefthead{"
header += "height:15px;"
header += "text-align:center;"
header += "background-color:#FFAA00;"
header += "color:#E8B388;"
header += "}</style>"
header += "</head>"
header += "<body>"
header += "<table cellspacing=0 cellpadding=0>"	
	
header1 = "</table>"
header1 += "</body>"
header1 += "</html>"

def getmid1():
    headword="<h5 style='white_space:nowrap;'>"+"大家好:"+"</h5>"
    headword+="<h5 style='white_space:nowrap;'>"+"风险策略监控如下表所示"+"</h5>"
    return headword

def getend():
	endword="<h4 style='white_space:nowrap;'>"+"如有问题，随时沟通"+"</h4>"
	endword+= "</body></html>"
	return endword

# 设定邮件发送的相关参数值
now = datetime.datetime.now()
today = now.strftime('%Y%m%d')
delta =datetime.timedelta(days=1)
yesterday=now-delta
yesterday=yesterday.strftime("%Y%m%d")
fromaddr = "caiyuxi@jd.com"
# toaddr = "bjzhaorui3@jd.com,guoxiaoinfo@jd.com,zhouchao1@jd.com,panglijuan@jd.com,malingyun1@jd.com,caoning3@jd.com,yuwanqing@jd.com,dushanli@jd.com,zhangxin93@jd.com,wangshun6@jd.com,haohongfei@jd.com"
# toaddr = "caiyuxi@jd.com,zhouchao1@jd.com,panglijuan@jd.com"
toaddr = "caiyuxi@jd.com"
msg = MIMEMultipart('related')
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = Header(u"【风险监控】策略日报-%s" % yesterday, 'utf-8')

strg=header1
strg+=getmid1()

strg+=header
rows=len(out_dt1)+1
cols=len(out_dt1.columns)	
strg+=gettable1(rows,cols,out_dt1)

strg+=header1
strg+=getend()

msgtext = MIMEText(strg, 'html', 'utf-8')
msg.attach(msgtext)

# send mail!
server = smtplib.SMTP()
server.connect("mx.jd.local", 25)
#server.starttls()
# server.login("risk_data", "PKpjnftqanw!336")
server.sendmail(fromaddr, toaddr.split(','), msg.as_string())
server.quit()	
