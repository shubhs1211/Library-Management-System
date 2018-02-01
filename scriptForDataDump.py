token = []

with open( '/Users/shubham/LMS/books.csv' ) as data:
    for line in data:
        tempArray = []
        for word in line.split('\t'):
            word = word.replace( "'", "''" )
            tempArray.append( word )
        token.append( tempArray )

# Write data from books.csv files to Library.sql file        
data = open( 'Library.sql', 'w')

data.write( "DROP SCHEMA IF EXISTS Library;\n" )

data.write( "CREATE SCHEMA Library;\n" )

data.write( "USE Library; \n\n\n " )

data.write( "CREATE TABLE BOOK( isbn varchar(10), title varchar(500), primary key(isbn));\n" )

data.write( "CREATE TABLE AUTHORS( author_id int, name varchar(50), primary key(author_id));\n")

data.write( "CREATE TABLE BOOK_AUTHORS( author_id int, isbn varchar(10), primary key(author_id,isbn), foreign key(author_id) references authors(author_id), foreign key(isbn) references book(isbn));\n" )

data.write( "CREATE TABLE BORROWER( Card_ID int, Ssn varchar(11),Bname varchar(50),Address varchar(100),Phone varchar(15), primary key(Card_ID), unique(Ssn));\n" )

data.write( "CREATE TABLE BOOK_LOANS( loan_id int, isbn varchar(10), card_id int, date_out date, due_date date, date_in date, primary key(loan_id), foreign key(isbn) references book(isbn), foreign key(card_id) references borrower(card_id) );\n" )

data.write( "CREATE TABLE FINES( loan_id int, fine_amt decimal(10,2), paid bool, primary key(loan_id), foreign key(loan_id) references book_loans(loan_id) );\n\n\n" )


# Table BOOK

bookArray = []
authorsArray = []
bookAuthorsArray = []

for i in token[ 1: ]:
    tempArray = []
    tempBookAuthorsArray=[]
    tempArray.append( i[0] )
    tempBookAuthorsArray.append( i[0] )
    tempArray.append( i[2] )
    tempBookAuthorsArray.append( i[2] )
    tempAuthorsArray = []
    for j in i[3].split(','):
        tempAuthorsArray.append( j )
    tempBookAuthorsArray.append( tempAuthorsArray )
    bookArray.append( tempArray )
    authorsArray.append( i[3] )
    bookAuthorsArray.append( tempBookAuthorsArray )

for i in bookArray:
    query = "INSERT INTO BOOK values('"+i[0]+"','"+i[1]+"');\n"
    data.write( query )

# Table AUTHORS

newAuthorsArray = []   
for i in authorsArray:
    for j in i.split( ',' ):
        newAuthorsArray.append( j )
newAuthorsArray = set( newAuthorsArray )
newTempAuthorsArray = []
for i in newAuthorsArray:
    newTempAuthorsArray.append(i)
authorId = []
for i in range(1, len( newTempAuthorsArray ) ):
    tempArray = []
    tempArray.append( i )
    tempArray.append( newTempAuthorsArray[i] )
    authorId.append( tempArray )
    query = "INSERT INTO AUTHORS values("+str(i)+",'"+newTempAuthorsArray[i]+"');\n"
    data.write( query )

# Table BOOK_AUTHORS

newBookAuthorsArray = []
for i in bookAuthorsArray:
    for j in i[2]:
        tempArray = []
        tempArray.append(i[0])
        for k in authorId:
            if( k[1] == j ):
                tempArray.append(k[0])
        if( len( tempArray ) == 2 ):
            newBookAuthorsArray.append( tempArray )

tempBookAuthorsArray = []
for i in newBookAuthorsArray:
    flag=0
    for j in tempBookAuthorsArray:
        if(i[0]==j[0] and j[1]==i[1]):
            flag = 1
            break;
    if( flag == 0 ):
        tempBookAuthorsArray.append(i)
for i in tempBookAuthorsArray:
    query = "INSERT INTO BOOK_AUTHORS values("+str(i[1])+",'"+str(i[0])+"');\n"
    data.write( query )

# Table BORROWER

borrowerArray = []
with open('/Users/shubham/LMS/borrowers.csv') as data:
    for line in data:
        tempArray = []
        for word in line.split( ',' ):
            word = word.replace( "\n", "" )            
            tempArray.append( word )
        borrowerArray.append( tempArray )

newBorrowerArray = []
for i in borrowerArray[ 1: ]:
    tempArray = []
    tempArray.append( i[0] )
    tempArray.append( i[1] )
    tempArray.append( i[2] +" "+ i[3] )
    combine = i[5]+", "+i[6]+", "+i[7]
    tempArray.append( combine )
    tempArray.append( i[8] )
    newBorrowerArray.append( tempArray )

# Write data from borrowers.csv files to Library.sql file     
data = open('Library.sql', 'a')
for i in newBorrowerArray:
    query = "INSERT INTO BORROWER values("+i[0]+",'"+i[1]+"','"+i[2]+"','"+i[3]+"','"+i[4]+"');\n"
    data.write(query)








