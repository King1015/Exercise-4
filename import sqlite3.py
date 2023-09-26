import sqlite3

# connect to database
conn = sqlite3.connect('library.db')
c = conn.cursor()

# create tables
c.execute('''CREATE TABLE IF NOT EXISTS Books
             (BookID TEXT PRIMARY KEY, Title TEXT, Author TEXT, ISBN TEXT, Status TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Users
             (UserID TEXT PRIMARY KEY, Name TEXT, Email TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Reservations
             (ReservationID TEXT PRIMARY KEY, BookID TEXT, UserID TEXT, ReservationDate TEXT)''')

# add new books to book table
def add_book():
    book_id = input("Enter Book ID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN: ")
    status = input("Enter Status: ")

    c.execute("INSERT INTO Books (BookID, Title, Author, ISBN, Status) VALUES (?, ?, ?, ?, ?)",
              (book_id, title, author, isbn, status))
    conn.commit()
    print("Book added successfully!")

# Find book details and booking status according to BookID
def find_book(book_id):
    c.execute('''SELECT Books.Title, Books.Status, Users.UserID, Users.Name, Users.Email
                 FROM Books
                 LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                 LEFT JOIN Users ON Reservations.UserID = Users.UserID
                 WHERE Books.BookID = ?''', (book_id,))
    result = c.fetchone()

    if result:
        title, status, user_id, name, email = result
        print("Title:", title)
        print("Status:", status)
        if user_id:
            print("Reserved by:")
            print("User ID:", user_id)
            print("Name:", name)
            print("Email:", email)
    else:
        print("Book not found!")

# Find the booking status of the book based on the criteria entered
def find_reservation():
    text = input("Enter BookID, UserID, ReservationID or Title: ")

    # Determine the type of input condition
    if text.startswith("LB"):
        c.execute('''SELECT Books.Status
                     FROM Books
                     WHERE Books.BookID = ?''', (text,))
        result = c.fetchone()

        if result:
            print("Reservation Status:", result[0])
        else:
            print("Book not found!")
    elif text.startswith("LU"):
        c.execute('''SELECT Books.Status, Books.Title
                     FROM Books
                     LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                     LEFT JOIN Users ON Reservations.UserID = Users.UserID
                     WHERE Users.UserID = ?''', (text,))
        result = c.fetchall()

        if result:
            print("Reservations:")
            for row in result:
                status, title = row
                print("Title:", title)
                print("Status:", status)
        else:
            print("No reservations found for this user!")
    elif text.startswith("LR"):
        c.execute('''SELECT Books.Status, Books.Title, Users.UserID, Users.Name, Users.Email
                     FROM Books
                     LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                     LEFT JOIN Users ON Reservations.UserID = Users.UserID
                     WHERE Reservations.ReservationID = ?''', (text,))
        result = c.fetchone()

        if result:
            status, title, user_id, name, email = result
            print("Title:", title)
            print("Status:", status)
            print("Reserved by:")
            print("User ID:", user_id)
            print("Name:", name)
            print("Email:", email)
        else:
            print("Reservation not found!")
    else:
        c.execute('''SELECT Books.Title, Books.Status, Users.UserID, Users.Name, Users.Email
                     FROM Books
                     LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                     LEFT JOIN Users ON Reservations.UserID = Users.UserID
                     WHERE Books.Title LIKE ?''', ('%' + text + '%',))
        result = c.fetchall()

        if result:
            print("Search results:")
            for row in result:
                title, status, user_id, name, email = row
                print("Title:", title)
                print("Status:", status)
                print("Reserved by:")
                print("User ID:", user_id)
                print("Name:", name)
                print("Email:", email)
        else:
            print("No matching books found!")

# Find details and reservation status for all books
def find_all_books():
    c.execute('''SELECT Books.BookID, Books.Title, Books.Status, Users.UserID, Users.Name, Users.Email
                 FROM Books
                 LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                 LEFT JOIN Users ON Reservations.UserID = Users.UserID''')
    result = c.fetchall()

    if result:
        print("All Books:")
        for row in result:
            book_id, title, status, user_id, name, email = row
            print("Book ID:", book_id)
            print("Title:", title)
            print("Status:", status)
            if user_id:
                print("Reserved by:")
                print("User ID:", user_id)
                print("Name:", name)
                print("Email:", email)
            print()
    else:
        print("No books found!")

# Modify the book information according to BookID
def modify_book(book_id):
    title = input("Enter new Title (or press Enter to skip modification): ")
    author = input("Enter new Author (or press Enter to skip modification): ")
    isbn = input("Enter new ISBN (or press Enter to skip modification): ")
    status = input("Enter new Status (or press Enter to skip modification): ")

    if title or author or isbn or status:
        c.execute("UPDATE Books SET Title=?, Author=?, ISBN=?, Status=? WHERE BookID=?",
                  (title, author, isbn, status, book_id))
        c.execute("UPDATE Reservations SET BookID=?, Status=? WHERE BookID=?",
                  (book_id, status, book_id))
        conn.commit()
        print("Book details updated successfully!")
    else:
        print("No modifications made!")

# Delete books according to BookID
def delete_book(book_id):
    c.execute("SELECT * FROM Reservations WHERE BookID=?", (book_id,))
    result = c.fetchone()

    if result:
        c.execute("DELETE FROM Reservations WHERE BookID=?", (book_id,))
    c.execute("DELETE FROM Books WHERE BookID=?", (book_id,))
    conn.commit()
    print("Book deleted successfully!")

# Main program loop
while True:
    print("Library Management System")
    print("1. Add a new book")
    print("2. Find a book's detail based on BookID")
    print("3. Find a book's reservation status")
    print("4. Find all the books")
    print("5. Modify book details based on BookID")
    print("6. Delete a book based on BookID")
    print("7. Exit")

    choice = input("Enter your choice (1-7): ")

    if choice == "1":
        add_book()
    elif choice == "2":
        book_id = input("Enter Book ID: ")
        find_book(book_id)
    elif choice == "3":
        find_reservation()
    elif choice == "4":
        find_all_books()
    elif choice == "5":
        book_id = input("Enter Book ID: ")
        modify_book(book_id)
    elif choice == "6":
        book_id = input("Enter Book ID: ")
        delete_book(book_id)
    elif choice == "7":
        break
    else:
        print("Invalid choice! Please try again.")

# Close database connection
conn.close()