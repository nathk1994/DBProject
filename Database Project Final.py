#Author: Nathan Keogh

from tkinter import *
import sqlite3

root = Tk() #TKinter creates the GUI window itself, also a widget.
root.title("Library Database Manager") #GUI window Title.
root.iconbitmap("C:\Dbicon3.ico") #sets an icon for the GUI, if not defined, the default KTinter feather icon is used, if incorrect file path, blank file icon is displayed.
root.geometry("400x500") #setting size of GUI window.



# create DB or connect to DB
connection = sqlite3.connect("Library_Database.db")

# create cursor
cursor = connection.cursor()

# create table , THIS ONLY NEEDS TO BE EXECUTED ONCE, commented out after first use, can be used to create a new table.

'''
cursor.execute("""CREATE TABLE Library (
            
            Book_ID integer NOT NULL unique,
            Section text NOT NULL,
            Title text NOT NULL,
            Author text NOT NULL,
            Year_Published integer NOT NULL,
            Available text NOT NULL
            
            )""")
'''



def SaveUpdate():
    # create DB or connect to DB
    connection = sqlite3.connect("Library_Database.db")

    # create cursor
    cursor = connection.cursor()

    record_update_id = delete_box.get()

    cursor.execute("""UPDATE Library SET 
        Book_ID = :ID,
        Section = :Sect,
        Title = :Ti,
        Author = :Auth,
        Year_Published = :YP,
        Available = :Avail
        
        WHERE Book_ID = :ID """, #Book_ID is primary key, used to search for results.
                   {
                    'ID': Book_ID_updater.get(),
                    'Sect': Section_updater.get(),
                    'Ti': Title_updater.get(),
                    'Auth': Author_updater.get(),
                    'YP': Year_Published_updater.get(),
                    'Avail': Available_updater.get()
                   })


    # commit changes to DB
    connection.commit()

    # close connection
    connection.close()

    #close window after button click
    updater.destroy()



#Create update record function, which opens a new GUI widget/window.
def Update():
    global updater
    updater = Tk()
    updater.title("Update a Record")  # GUI window Title.
    updater.iconbitmap("C:\Dbicon3.ico")  # sets an icon for the GUI, if not defined, the default KTinter feather icon is used, if incorrect file path, blank file icon is displayed.
    updater.geometry("400x250")  # setting size of GUI window.

    # create DB or connect to DB
    connection = sqlite3.connect("Library_Database.db")

    # create cursor
    cursor = connection.cursor()

    record_update_id = delete_box.get() #to get the data from the select book ID entry box
    # "Query" the Database
    cursor.execute("SELECT * FROM Library WHERE Book_ID=" + record_update_id)  # SQL SELECT statement to display all results from database & oid is a built in PRIMARY KEY for the SQLite module, starts at 1.
    records = cursor.fetchall()  # variable for printing variable in terminal

    # loop through results, to get more than 1 result.
    print_records = " "
    for record in records:  # prints everything, calls all items.
        print_records += str(record) + "\n"

    #Create GLOBAL variable for text box names
    global Book_ID_updater
    global Section_updater
    global Title_updater
    global Author_updater
    global Year_Published_updater
    global Available_updater

    # CREATE THE TEXT BOXES HERE
    # book ID
    Book_ID_updater = Entry(updater, width=30)
    Book_ID_updater.grid(row=0, column=1, padx=20, pady=(10, 0))
    # Section
    Section_updater = Entry(updater, width=30)
    Section_updater.grid(row=1, column=1, padx=20)
    # Title
    Title_updater = Entry(updater, width=30)
    Title_updater.grid(row=2, column=1, padx=20)
    # Author
    Author_updater = Entry(updater, width=30)
    Author_updater.grid(row=3, column=1, padx=20)
    # Year published
    Year_Published_updater = Entry(updater, width=30)
    Year_Published_updater.grid(row=4, column=1, padx=20)
    # Available (Y/N)
    Available_updater = Entry(updater, width=30)
    Available_updater.grid(row=5, column=1, padx=20)


    # CREATE THE TEXT BOX LABELS HERE
    Book_ID_label = Label(updater, text="Book ID")
    Book_ID_label.grid(row=0, column=0, pady=(10, 0))

    Section_label = Label(updater, text="Section")
    Section_label.grid(row=1, column=0)

    Title_label = Label(updater, text="Title")
    Title_label.grid(row=2, column=0)

    Author_label = Label(updater, text="Author")
    Author_label.grid(row=3, column=0)

    Year_Published_label = Label(updater, text="Year Published")
    Year_Published_label.grid(row=4, column=0)

    Available_label = Label(updater, text="Available (Y/N)")
    Available_label.grid(row=5, column=0)

    # Loop through results, populates the text boxes.
    for record in records:
        Book_ID_updater.insert(0, record[0])
        Section_updater.insert(0, record[1])
        Title_updater.insert(0, record[2])
        Author_updater.insert(0, record[3])
        Year_Published_updater.insert(0, record[4])
        Available_updater.insert(0, record[5])

    # Create a Save Updated records button
    update_button = Button(updater, text="Save Updated Record", command=SaveUpdate)
    update_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=140)





#Create SUBMIT  to DB function
def submit():
    # create DB or connect to DB
    connection = sqlite3.connect("Library_Database.db")

    # create cursor
    cursor = connection.cursor()

    #Insert into Table , Executes the SQL statement insert to store data entered from text boxes.
    cursor.execute("INSERT INTO Library VALUES (:Book_ID, :Section, :Title, :Author, :Year_Published, :Available)",
                {

                    'Book_ID': Book_ID.get(),
                    'Section': Section.get(),
                    'Title': Title.get(),
                    'Author': Author.get(),
                    'Year_Published': Year_Published.get(),
                    'Available': Available.get()

                })

    # commit changes to DB
    connection.commit()

    # close connection
    connection.close()



    #Clear the text boxes
    Book_ID.delete(0, END)
    Section.delete(0, END)
    Title.delete(0, END)
    Author.delete(0, END)
    Year_Published.delete(0, END)
    Available.delete(0, END)



# Function to Delete
def delete():
    # create DB or connect to DB
    connection = sqlite3.connect("Library_Database.db")

    # create cursor
    cursor = connection.cursor()

    # Delete function
    cursor.execute("DELETE from Library WHERE Book_ID=" + delete_box.get()) #SQL to delete a record, by getting entry from the Text box input.

    delete_box.delete(0, END) # Clears the text box.

    # commit changes to DB
    connection.commit()

    # close connection
    connection.close()


#Show Records Function
def ShowRecords():
    # create DB or connect to DB
    connection = sqlite3.connect("Library_Database.db")

    # create cursor
    cursor = connection.cursor()

    #"Query" the Database
    cursor.execute("SELECT * FROM Library")#SQL SELECT statement to display all results from database & oid is a built in PRIMARY KEY for the SQLite module, starts at 1.
    records = cursor.fetchall()#variable for printing variable in terminal
    # print(records) #testing it works in terminal, commented out in end as no longer needed, was useful for troubleshooting.

    #loop through results, to get more than 1 result.
    print_records = " "
    for record in records: #prints everything, calls all items.
        print_records += str(record) + "\n" #for creating a label, so each item is printed out on their own line. cant concaninate string with int. each records is an item now, is a tuple, inside of that it has item numbers, tupple numbers.

    #Show Records Label ,
    show_label = Label(root, text=print_records)
    show_label.grid(row=8, column=0, columnspan=2)

    # commit changes to DB
    connection.commit()

    # close connection
    connection.close()



            #KTinter - Designing the GUI.

#CREATE THE TEXT BOXES HERE
#book ID
Book_ID = Entry(root,width=30)
Book_ID.grid(row=0, column=1, padx=20, pady=(10,0))
#Section
Section = Entry(root,width=30)
Section.grid(row=1, column=1, padx=20)
#Title
Title = Entry(root,width=30)
Title.grid(row=2, column=1, padx=20)
#Author
Author = Entry(root,width=30)
Author.grid(row=3, column=1, padx=20)
#Year published
Year_Published = Entry(root,width=30)
Year_Published.grid(row=4, column=1, padx=20)
#Available (Y/N)
Available = Entry(root,width=30)
Available.grid(row=5, column=1, padx=20)

#DELETE Record TEXT Box
delete_box = Entry(root, width=30)
delete_box.grid(row=9, column=1)


#CREATE THE TEXT BOX LABELS HERE
Book_ID_label = Label(root,text="Book ID")
Book_ID_label.grid(row=0, column=0, pady=(10,0))

Section_label = Label(root,text="Section")
Section_label.grid(row=1, column=0)

Title_label = Label(root,text="Title")
Title_label.grid(row=2, column=0)

Author_label = Label(root,text="Author")
Author_label.grid(row=3, column=0)

Year_Published_label = Label(root,text="Year Published")
Year_Published_label.grid(row=4, column=0)

Available_label = Label(root,text="Available (Y/N)")
Available_label.grid(row=5, column=0)

#DELETE Record TEXT Box LABEL
Delete_Button_Label= Label(root,text="Select by Book ID ->")
Delete_Button_Label.grid(row=9, column=0)

#BUTTONS

#Create Delete Button
delete_button = Button(root, text= "Delete Record", command=delete)
delete_button.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

#Create Add Record to Database Button
submit_button = Button(root, text="Add Record to Database", command=submit)
submit_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

#Create Show records button
show_button = Button(root, text= "Show Records", command=ShowRecords)
show_button.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

#Create Update records button
update_button = Button(root, text= "Update Record", command=Update)
update_button.grid(row=12, column=0, columnspan=2, pady=10, padx=10, ipadx=140)

#Close Application button
button_quit = Button(root, text="Exit Program", command=root.quit)
button_quit.grid(row=13, column=0, columnspan=2, pady=10, padx=10, ipadx=140)

# commit changes to DB
connection.commit()

# close connection
connection.close()

#loop the widget(Application GUI)
root.mainloop()