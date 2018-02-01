# from __future__ import unicode_literals
from __future__ import division
from django.template import Template, Context
from dateutil.relativedelta import relativedelta
from django.views.decorators import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import Context, Template
from django.template import Template
from django.contrib import messages
from django.template import Library, Template
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe
from django.utils import timezone
from datetime import datetime
from django.db import connection
from datetime import datetime
from random import randint
import ast
import urllib
import random
import time
import collections
import re

pattern = re.compile("^[\d[0-9]{3}[\d[0-9]{3}[\d[0-9]{4}$", re.IGNORECASE)


def index(request):
	return render(request, 'index.html')
	
def search(request):
	if request.GET['ita']:
		ita = request.GET['ita']
	ita = str([ita][0])
	cursor = connection.cursor()
	cursor.execute("Select book.isbn,book.title,group_concat(DISTINCT authors.name) as name from book JOIN book_authors ON book.isbn = book_authors.isbn JOIN authors ON book_authors.author_id = AUTHORS.author_id  where book.isbn LIKE %s or book.title LIKE %s or authors.name LIKE %s group by book.isbn" , (['%%'+ita+'%%'],['%%'+ita+'%%'],['%%'+ita+'%%']))
	data=[[str(r[0]),r[1].encode('utf-8'),r[2].encode('utf-8')] for r in cursor.fetchall()]
	cursor.close()
	return render(request, 'results.html' , {'data': data, 'ita' : ita})

def checkout(request):
	return render(request, 'checkout.html')

def checkoutbook(request):
	if request.GET['book']:
		book = request.GET['book']
	if request.GET['cardnumber']:
		cardno = request.GET['cardnumber']

	cardno = str(cardno)
	cursor = connection.cursor()
	cursor.execute("Select isbn from book where title=%s", [book])
	isbn = cursor.fetchall()
	cursor.close()

	cursor = connection.cursor()
	cursor.execute("Select COUNT(*) from book_loans where date_in IS NULL and isbn = %s", [isbn])
	count = cursor.fetchall()
	print count
	cursor.close()
	if int(count[0][0]) == 1:
		html = "<html><head><script type='text/javascript'> alert('Book already checked out'); window.location = '/checkout/';</script></head></html>"
		return HttpResponse(html)
	else:
		cursor = connection.cursor()
		cursor.execute("Select COUNT(*) from book_loans where date_in IS NULL and card_id=%s", [cardno])
		count = cursor.fetchall()
		cursor.close()
		if int(count[0][0]) > 2:
			html = "<html><head><script type='text/javascript'> alert('You have already borrowed 3 books'); window.location = '/checkout/';</script></head></html>"
			return HttpResponse(html)
		else:
			cursor = connection.cursor()
			cursor.execute("Select max(loan_id) FROM book_loans")
			loan_id_max = cursor.fetchall()
			cursor.close()
			loan_id = randint(000000,999999);
	    	cursor = connection.cursor()
	    	cursor.execute("Select isbn FROM book WHERE title = %s ",[book])
	    	isbn = cursor.fetchall()
	    	isbn = str(isbn[0][0])
	    	cursor.close()
	    	date_out = time.strftime("%Y/%m/%d")
	    	print "date out",type(date_out)
	    	date_after_14_days = datetime.now()+ relativedelta(days=14)
	    	due_date = date_after_14_days.strftime('%Y/%m/%d')
	    	date_in = None

	    	cursor = connection.cursor()
	    	cursor.execute("Insert into book_loans values(%s,%s ,%s,%s,%s,%s)",([loan_id],[isbn],[cardno],[date_out],[due_date],[date_in]))
	    	cursor.close()
	    	html = "<html><head><script type='text/javascript'> alert('Book added to you account'); window.location = '/checkout/';</script></head></html>"
	    	return HttpResponse(html)

def checkin(request):
	return render(request, 'checkin.html')


def checkinbook(request):
	if request.GET['checkin']:
		checkin = request.GET['checkin']
	data = []
	checkin = str([checkin][0])
	cursor = connection.cursor()
	cursor.execute("select isbn from book_loans natural join borrower where date_in is null and card_id = %s or isbn like %s or bname like %s" , ([checkin],['%%'+checkin+'%%'],['%%'+checkin+'%%']))
	
	data_out = [] 
	list_isbn = cursor.fetchall()
	if len(list_isbn) > 0:
		for isbn in list_isbn:
			data = []
			data.append(str(isbn[0]))
			cursor = connection.cursor()
			cursor.execute("Select card_id from book_loans where isbn = %s and date_in IS NULL", [str(isbn[0])])
			card_id = cursor.fetchall()
			card_id = str(card_id[0][0])
			data.append(card_id)
			
			cursor = connection.cursor()
			cursor.execute("Select title from book where isbn = %s", [str(isbn[0])])
			title = cursor.fetchall()
			title = str(title[0][0])
			data.append(title)
			data_out.append(data)
	else:
		html = "<html><head><script type='text/javascript'> alert('No Books to Checkin'); window.location = '/checkin/';</script></head></html>"
		return HttpResponse(html)
	cursor.close()
	return render(request, 'results2.html', {'data':data_out})




def borrower(request):
	return render(request, 'borrower.html')

def createborrower(request):
	
	if request.GET['ssn']:
		ssn = request.GET['ssn']
	if request.GET['name']:
		name = request.GET['name']
	if request.GET['address']:
		address = request.GET['address']
	if request.GET['phone']:
		phone = request.GET['phone']

	ssn = str((ssn))
	ssn_list = list(ssn)
	if pattern.match(str(phone)):
		if ssn_list[3] == '-' and ssn_list[6] == '-':

			cursor = connection.cursor()
			cursor.execute("select max(card_id) FROM borrower")
			cardnumber_max = cursor.fetchone()
			cursor.close()
			cardnumber = int(cardnumber_max[0]) + 1
			cursor = connection.cursor()
			cursor.execute("select count(*) from borrower where ssn =%s",([ssn]))
			count = cursor.fetchall()
			cursor.close()
			

			if int(count[0][0]) == 1 or int(count[0][0]) > 1:
				
				html = "<html><head><script type='text/javascript'> alert('SSN already exists!'); window.location = '/borrower/';</script></head></html>"
				return HttpResponse(html)
			else:
				cursor = connection.cursor()
				cursor.execute("Insert into borrower values(%s,%s,%s,%s,%s)",([cardnumber],[ssn],[name],[address],[phone]))
				cursor.close()
		  		html = "<html><head><script type='text/javascript'> alert('Borrower successfully updated!'); window.location = '/borrower/';</script></head></html>"
				return HttpResponse(html)
		else :
			html = "<html><head><script type='text/javascript'> alert('Enter Valid SSN'); window.location = '/borrower/';</script></head></html>"
			return HttpResponse(html)

	else : 
		html = "<html><head><script type='text/javascript'> alert('Enter Valid Phone Number'); window.location = '/borrower/';</script></head></html>"
		return HttpResponse(html)


def updatepay(request,x):
	l = str(x)
	l = l.split('.')
	print "Hi",l
	loan_id = l[0]
	card_id = l[1]
	print loan_id
	cursor = connection.cursor()
	cursor.execute("update fines set paid=1 where loan_id=%s", ([loan_id]))
	html = "<html><head><script type='text/javascript'> alert('Fine Paid'); window.location = '/borrower/';</script></head></html>"
	return HttpResponseRedirect(html)		
		
def updatebookloans(request,x):
	l = str(x)
	l = l.split('.')
	isbn = l[0]
	card_id = l[1]
	date_in = l[2]
	cursor = connection.cursor()
	cursor.execute("update book_loans set date_in=%s where isbn=%s and card_id=%s", ([date_in],[isbn],[card_id]))
	html = "<html><head><script type='text/javascript'> alert('Your book has been returned'); window.location = '/borrower/';</script></head></html>"
	return HttpResponseRedirect(html)


def updatefine(request):
	return render(request, 'updatefines.html')

def updatefineform(request):
	if request.GET['update']:
		update = request.GET['update']
	print str(update)
	if str(update) != datetime.strptime(str(update), "%Y-%m-%d").strftime('%Y-%m-%d'):
		html = "<html><head><script type='text/javascript'> alert('Enter Valid Date'); window.location = '/updatefine/';</script></head></html>"
		return HttpResponse(html)
	else:
		cursor = connection.cursor()
		cursor.execute("select loan_id, due_date from book_loans where date_in IS NULL and due_date < %s",([update]))
		data_list = list(cursor.fetchall())
		for each in data_list:
			cursor =  connection.cursor()
			cursor.execute("select loan_id from fines where loan_id = %s and paid = 0",([str(each[0])]))
			if len(cursor.fetchall())  > 0 :
				cursor.execute("update fines set fine_amt=((SELECT DATEDIFF(%s,%s) AS days)*0.25) where loan_id=%s", ([update], [str(each[1])], [str(each[0])]))
			else:
				cursor.execute("insert into fines values(%s,(SELECT DATEDIFF(%s,%s) AS days)*0.25,FALSE)", ([str(each[0])],[update], [str(each[1])]))
	html = "<html><head><script type='text/javascript'> alert('fines updated'); window.location = '/updatefine/';</script></head></html>"
	return HttpResponse(html)
				
def payfine(request):
	return render (request, 'fines.html')

def payfinesform(request):
	if request.GET['cardnumber']:
		cardnumber = request.GET['cardnumber']
		cursor =connection.cursor()
		cursor.execute("select * from book_loans natural join fines where card_id=%s",([cardnumber]))
		list_data = list(cursor.fetchall())
		data_out = []
		for each in list_data:
			data = []
			data.append(each[0])
			data.append(each[1])
			data.append(each[2])
			data.append(each[6])
			data_out.append(data)
			
		# for each in list_data:
			# cursor =  connection.cursor()
			# cursor.execute("update fines set fine_amt=((SELECT DATEDIFF(%s,%s) AS days)*0.25) where loan_id=%s", ([str(each[4])],[str(each[5])],[str(each[0])]))
			
		# cursor = connection.cursor()
		# cursor.execute("select loan_id, due_date from book_loans where date_in > due_date",)
		# data_list = list(cursor.fetchall())
		# for each in data_list:
			# cursor =  connection.cursor()
			# cursor.execute("update fines set fine_amt=((SELECT DATEDIFF(%s,%s) AS days)*0.25) where loan_id=%s", ([str(each[4])],[str(each[5])],[str(each[0])]))
		
		cursor.execute("select sum(fine_amt) from fines natural join book_loans where card_id=%s and paid=0 group by card_id",([cardnumber]))
		sum_amt = cursor.fetchall()
		print sum_amt
		if sum_amt == ():
			return render (request, 'fines.html')
		else:
			sum_amt = str(sum_amt[0])
			# print sum_amt
			if sum_amt  > 0:
				total_fine = sum_amt
				print "Total fine is", total_fine
			else:
				total_fine = 0
				print "Total fine is 0"
			return render(request, 'payfines.html', {'data': data_out,'total_fine': total_fine})
		
	
	

		
