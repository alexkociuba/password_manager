from tkinter import *
import random
from tkinter import messagebox
import pyperclip
import json



# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letter_char = [random.choice(letters) for _ in range(random.randint(3, 6))]
    symbol_char = [random.choice(symbols) for _ in range(random.randint(3, 6))]
    number_char = [random.choice(numbers) for _ in range(random.randint(3, 6))]

    password_list = letter_char + symbol_char + number_char
    random.shuffle(password_list)

    password = "".join(password_list)

    # enters the generated password to the password field when the generate button is clicked
    password_entry.insert(0, password)
    # copies to clipboard
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    username = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": username,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Warning", message="fix missing fields")
    else:
        try:
            with open("password_file.json", "r") as data_file:
                # read old data
                data = json.load(data_file)
        except json.decoder.JSONDecodeError:
            with open("password_file.json", "w") as data_file:
                # updating old data with new data
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)

            with open("password_file.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    website = website_entry.get()


    try:
        with open("password_file.json") as data_file:
            data = json.load(data_file)
            if website in data:
                password_result = data[website]["password"]
                username_result = data[website]["email"]
                password_entry.insert(0, password_result)
                email_entry.insert(0, username_result)
            elif website not in data:
                # password_entry.insert(0, "NOT found")
                messagebox.showwarning(title="Warning", message="Nothing Found!")
    except json.decoder.JSONDecodeError:
        print("Error nothing found")





# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo4i.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=0, columnspan=3)

# labels
version_number = Label(text="ver 1.1")
version_number.grid(row=5, column=2)
website_label = Label(text="website")
website_label.grid(row=1, column=0)
e_mail_label = Label(text="e-mail")
e_mail_label.grid(row=2, column=0)
password_label = Label(text="password")
password_label.grid(row=3, column=0)

# entries
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1, columnspan=1)
website_entry.focus()
email_entry = Entry(width=21)
email_entry.grid(row=2, column=1, columnspan=1)
email_entry.insert(0, "test@gmail.com")
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# buttons
generate_button = Button(width=12, text="generate", command=password_generator)
generate_button.grid(row=3, column=2)
add_button = Button(width=30, text="add", command=save)
add_button.grid(row=4, column=1, columnspan=2, pady=5, padx=5)
search_button = Button(width=12, text="search", command=find_password)
search_button.grid(row=1, column=2)

window.mainloop()
