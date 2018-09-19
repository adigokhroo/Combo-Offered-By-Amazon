from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.conf.urls import include, url
from combo.register.models import Document
from combo.register.forms import DocumentForm
import codecs
from django.db.models.query_utils import DeferredAttribute
from combo.register.nphard import subset_sum
import csv
import os
import itertools
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


def home(request):
	documents = Document.objects.all()
	return render(request, 'register/home.html', {'documents': documents})


def model_form_upload(request):
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)

		if form.is_valid():
			form.save()

			data = form.cleaned_data
			num = data['range']
			

			#num = form.cleaned_data[range]
			file_name = Document.filename

			for filename in request.FILES:
				file_name = request.FILES[filename].name

			path1 = "C:\\Users\\mayank jain\\Desktop\\projects\\combo\\media\\documents"
			path2 = os.path.join(path1, file_name)


			with open(path2, mode='r') as infile:
				reader = csv.reader(infile)
				with open('test_new.csv', mode='w') as outfile:
					writer = csv.writer(outfile)
					mydict = {rows[0]:rows[1] for rows in reader}

			mydict = {k:int(v) for k,v in mydict.items()}


			with open(path2,mode='a',newline='') as f:
				for comb in itertools.combinations(mydict.keys(), 4):
					if sum(mydict[k] for k in comb) == num:
						writer = csv.writer(f,delimiter=',')
						writer.writerow(comb)
						writer.writerow([])


			def send_mail(send_from = "mayankj29121996@gmail.com",send_to = "aditya19.gokhroo@gmail.com",subject = "Your generated combo offer",text = "Congratulations  amazon we have generated the following csv file related to the available offers we had", files="test1.csv",server="127.0.0.1"):
				assert isinstance(send_to, list)

				msg = MIMEMultipart()
				msg['From'] = send_from
				msg['To'] = COMMASPACE.join(send_to)
				msg['Date'] = formatdate(localtime=True)
				msg['Subject'] = subject

				msg.attach(MIMEText(text))

				for f in files or []:
					with open(f, "rb") as fil:
						part = MIMEApplication(
							fil.read(),
							Name=basename(f)
						)
						part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
						msg.attach(part)


				smtp = smtplib.SMTP(server)
				smtp.sendmail(send_from, send_to, msg.as_string())
				smtp.close()


		else:
			print(form.errors)
			print(request.FILES)
			return redirect('home')

	else:
		form = DocumentForm()

	return render(request, 'register/model_form_upload.html', {
		'form': form,
	})
