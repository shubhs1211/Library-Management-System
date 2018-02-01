-------------------------------- README FILE ------------------------------------

This project is created and tested on a Mac  machine. 

Frameworks used :
1. Django 1.11.6 

Languages used :
1. Python 2.7.10
2. MYSQL 5.7
3. HTML
4. CSS
5. JavaScript
6. Ajax
7. AngularJS


Libraries/packages used: 
1. mysql-connector-(2.1.4)
2. mysql-python (1.2.5)
3. python-dateutil (2.6.0)
4. pytz (2016.10)
5. pip (9.0.1)
6. pyparsing (2.1.10)
7. virtualenv (15.1.0)(Optional)
8. bootstrap-toolkit


How to Compile:

Install the necessary packages first.


1. Start the Terminal on Mac
2. Navigate to the project directory -> cd 'path'
3. Modify 'scriptForDataDump.py' by editing the path of 'books.csv' and 'borrowers.csv' files.run 'python scriptForDataDump.py'. 	This will generate library.sql file.
4. Start the MySQL server by typing 'mysql -u root -p' and providing the root   
   password.
5. Now enter the data into the database by using the following commands:
	- CREATE DATABASE Library;
	- USE Library;
	- source 'path of the Library.sql file'
6. Make changes in 'settings.py' by setting your own root password for mysql. Also set the paths in 'TEMPLATES_DIRS' and 	
	'STATICFILES_DIRS'
7. Open new terminal window and Navidate to project directory which contains the file manage.py
8. To run the project: 
	- "python manage.py migrate"
	- "python manage.py runserver"
9. Open your web browser and type the ip address given on the terminal 
eg. http://127.0.0.1:8000/ to access the UI




 
