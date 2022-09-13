the qr-gen.py is to generate qr code for given input text

the qr-read.py is to read image data from camera or use the image-file to read images

robot.py is to control the robot based on the images shown

the GUI interface is not connected with the above mentioned files .

to run gui interface u should install django
to start the webpage run this in terminal:
python3 manage.py runserver
and in browser go to webpage : 127.0.0.1:8000/med 

in add page enter the details of first patient and select between m1 to m6 for the patient's medicines . once details are filled go to home and press start

if you want to check the entered details go to show data page form the home page. you can also delete data from the show page.

if you need to see what happens in the database i.e db.sqlite3 install DB browser (SQLite) to view it

the new folder has a few generated qr-codes to test and use