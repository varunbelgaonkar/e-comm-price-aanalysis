from tkinter import *
from test import get_amaz_values
from flipkart_products import get_flipkart_values
import threading
from send_email import send_email
from tkinter import messagebox

root = Tk()
root.title("Price comaparison")
root.geometry("500x500")


def get_values():
	item = e.get()
	t1 = threading.Thread(target = get_amaz_values, args=[item])
	t2 = threading.Thread(target = get_flipkart_values , args = [item])
	t1.start()
	t2.start()
	t1.join()
	t2.join()

def send_mail():
	global e_email
	e_email = Entry(root, width = 50, borderwidth=5)
	e_label = Label(root, text="Enter your email: ", padx=10, pady=10)
	send_button = Button(root, text="Send", padx=10, pady=10, command=send)
	e_email.grid(row=2, column=1, columnspan=3)
	e_label.grid(row=2, column=0)
	send_button.grid(row=3, column=1)

def send():
	mail = e_email.get()
	send_email(mail)
	messagebox.showinfo("Email", "Email Sent!")


#creating widgets
label = Label(root, text="Enter product name: ", padx = 10, pady = 10)
e = Entry(root, width = 50, borderwidth = 5)
search_button = Button(root, text = "Search", padx = 10, 
					 pady = 10, command = get_values)
exit_button = Button(root, text = "Exit", padx = 10,
					 pady = 10, command = root.quit)
email_button = Button(root, text = "Email", padx = 10,
					 pady = 10, command = send_mail)

#placing the widgets
label.grid(row=0, column = 0)
e.grid(row=0, column = 1, columnspan = 3 )
search_button.grid(row=1, column=2,)
exit_button.grid(row=1, column=1)
email_button.grid(row = 1, column = 0)

root.mainloop()
