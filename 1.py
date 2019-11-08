import requests
import re
import json
import time
import os.path
import smtplib
from email.mime.text import MIMEText


def SendEmails(al):

	msg_from='' 
	                               #发送方邮箱
	passwd=''                                   #填入发送方邮箱的授权码
	msg_to=''
	msg_to1=''                                #收件人邮箱                      
	subject="最新咨询"                                     #主题     
	content=al   #正文
	msg = MIMEText(content)
	msg['Subject'] = subject
	msg['From'] = msg_from
	msg['To'] = msg_to

	s = smtplib.SMTP_SSL("smtp.qq.com",465)#邮件服务器及端口号
	s.login(msg_from, passwd)
	s.sendmail(msg_from, msg_to, msg.as_string())
	s.sendmail(msg_from, msg_to1, msg.as_string())
	print ("发送成功")



pd=0
xz=0
while(True):
	print ("循环开始")
	print (pd)
	a1=""
	# 360
	url="https://cert.360.cn/weibo/get"

	html=requests.get(url).text.encode()
	if len(html)!=pd:
		pd=len(html)
		html=eval(html)
		times=time.strftime("%Y-%m-%d", time.localtime())
		filename=times+".txt"
		al=a1+"360咨询:\n"
		
		with open(filename,'w',encoding='utf-8') as f:
			for i in html:
				print (i['created_at_str'])
				print (i['text'])
				s=i['created_at_str']+"\n"+i['text']+"\n\n"
				al=al+s
				print (al)
				f.write(s)	
			print (al)


	url="https://xz.aliyun.com/"
	times=time.strftime("%Y-%m-%d", time.localtime())
	html=requests.get(url).text
	if(xz!=len(html)):
		al=al+"先知咨询\n"
		xz_s=re.findall(r'<tr>(.*?)</tr>',html,re.S)
		for i in xz_s:
			s=re.search(r'/ (.*?)\n',i,re.S)
			s=s.group()[2:12]
			if(s==times):
				s1=re.search(r'class="topic-title" href="(.*?)"',i,re.S)
				sz=s1.group()
				s1=s1.group()[:-1]
				s1=s1[26:]
				s1="https://xz.aliyun.com"+s1
				sz=sz+">(.*?)"+r"</a>"
				s2=re.findall(sz,i,re.S)
				s2=s2[0].strip()
				print(s2)
				al=al+s2+"\n"+s1+"\n\n"
				print (s1)
	print (a1)
	SendEmails(al)		


	time.sleep(1800)


