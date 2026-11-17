# Library Book Management System

class Book:

    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

    def display(self):
        print("Book Title:", self.title)
        print("Author Name:", self.author)
        print("Price: ₹", self.price)

        if self.price >= 1000:
            print("Category: Premium")
        elif self.price >= 500:
            print("Category: Standard")
        else:
            print("Category: Basic")

        print("------------------------")


class Library:

    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def display_books(self):
        print("\nLIBRARY BOOK DETAILS")
        print("====================")

        for book in self.books:
            book.display()


# CO1 - Library Book Management

library = Library()

n = int(input("Enter number of books: "))

for i in range(n):

    print("\nEnter details of book", i + 1)

    title = input("Enter Book Title: ")
    author = input("Enter Author Name: ")
    price = float(input("Enter Price: "))

    book = Book(title, author, price)

    library.add_book(book)

library.display_books()


# CO2 - Climbing Stairs using Dynamic Programming

print("\nCLIMBING STAIRS PROBLEM")
print("=======================")

stairs = int(input("Enter number of stairs: "))

if stairs == 0:
    ways = 1

elif stairs == 1:
    ways = 1

else:
    dp = [0] * (stairs + 1)

    dp[0] = 1
    dp[1] = 1

    for i in range(2, stairs + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    ways = dp[stairs]

print("Number of ways to climb", stairs, "stairs:", ways)