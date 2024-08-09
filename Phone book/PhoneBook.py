from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import re  
from views import *

# Colors
color0 = "#ffffff"
color1 = "#000000"
color2 = "#152eff"

# Window setup
window = Tk()
window.title("Phone Book")
window.geometry("485x450")
window.configure(background=color0)
window.resizable(width=FALSE, height=FALSE)

# Frames
frame_up = Frame(window, width=500, height=50, background=color2)
frame_up.grid(row=0, column=0, padx=0, pady=1)

frame_down = Frame(window, width=500, height=150, background=color0)
frame_down.grid(row=1, column=0, padx=0, pady=1)

frame_table = Frame(window, width=500, height=100, background=color0, relief="flat")
frame_table.grid(row=2, column=0, columnspan=2, padx=10, pady=1, sticky=NW)

# Functions
def show():
    global tree

    list_header = ["Name", "Gender", "Telephone", "Email"]
    demo_list = view()

    tree = ttk.Treeview(frame_table, selectmode="extended", columns=list_header, show="headings")

    vsb = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame_table, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky="nsew")
    vsb.grid(column=1, row=0, sticky="ns")
    hsb.grid(column=0, row=1, sticky="ew")

    # Tree headings
    tree.heading(0, text="NAME", anchor=NW)
    tree.heading(1, text="GENDER", anchor=NW)
    tree.heading(2, text="TELEPHONE", anchor=NW)
    tree.heading(3, text="EMAIL", anchor=NW)

    # Tree columns
    tree.column(0, width=110, anchor="nw")
    tree.column(1, width=110, anchor="nw")
    tree.column(2, width=120, anchor="nw")
    tree.column(3, width=110, anchor="nw")

    for item in demo_list:
        tree.insert("", "end", values=item)

show()

def validate_input(name, gender, telephone, email):
    if not name or not gender or not telephone or not email:
        messagebox.showwarning("Validation Error", "All fields are required!")
        return False
    if not re.match(r"^\+?\d{10,15}$", telephone):
        messagebox.showwarning("Validation Error", "Enter a valid telephone number (10-15 digits)!")
        return False
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        messagebox.showwarning("Validation Error", "Enter a valid email address!")
        return False
    return True

def insert():
    name = entry_name.get()
    gender = combo_gender.get()
    telephone = entry_telephone.get()
    email = entry_email.get()

    if validate_input(name, gender, telephone, email):
        data = [name, gender, telephone, email]
        add(data)
        messagebox.showinfo("Data", "Contact added successfully!")

    entry_name.delete(0, "end")
    combo_gender.set("")
    entry_telephone.delete(0, "end")
    entry_email.delete(0, "end")

    show()

def to_update():
    try:
        tree_data = tree.focus()
        tree_dictionary = tree.item(tree_data)
        tree_list = tree_dictionary["values"]

        name = str(tree_list[0])
        gender = str(tree_list[1])
        telephone = str(tree_list[2])
        email = str(tree_list[3])
        
        entry_name.delete(0, "end")
        entry_name.insert(0, name)

        combo_gender.set(gender)

        entry_telephone.delete(0, "end")
        entry_telephone.insert(0, telephone)

        entry_email.delete(0, "end")
        entry_email.insert(0, email)

        def confirm():
            new_name = entry_name.get()
            new_gender = combo_gender.get()
            new_telephone = entry_telephone.get()
            new_email = entry_email.get()

            if validate_input(new_name, new_gender, new_telephone, new_email):
                if messagebox.askyesno("Confirm Update", "Are you sure you want to update this contact?"):
                    data = [telephone, new_name, new_gender, new_telephone, new_email]
                    update(data)
                    messagebox.showinfo("Success", "Contact updated successfully")

                    entry_name.delete(0, "end")
                    combo_gender.set("")
                    entry_telephone.delete(0, "end")
                    entry_email.delete(0, "end")

                    for widget in frame_table.winfo_children():
                        widget.destroy()

                    button_confirm.destroy()

                    show()
        
        button_confirm = Button(frame_down, text="Confirm", width=10, height=1, background=color2, foreground=color0, font="Ivy 8 bold", command=confirm)
        button_confirm.place(x=237, y=110)
    except IndexError:
        messagebox.showerror("Error", "Select a contact from the table to update!")
    

def to_remove():
    try:
        tree_data = tree.focus()
        tree_dictionary = tree.item(tree_data)
        tree_list = tree_dictionary["values"]
        tree_telephone = str(tree_list[2])

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?"):
            remove(tree_telephone)
            messagebox.showinfo("Success", "Data successfully deleted")

            for widget in frame_table.winfo_children():
                widget.destroy()

            show()

    except IndexError:
        messagebox.showerror("Error", "Select a contact from the table to delete!")

def to_search():
    telephone = entry_search.get()
    data = search(telephone)

    def delete_command():
        tree.delete(*tree.get_children())
    
    delete_command()

    for item in data:
        tree.insert("", "end", values=item)
        
    entry_search.delete(0, "end")

# Frame_down widgets
app_name = Label(frame_up, text="PHONE BOOK", height=1, font="Verdana 17 bold", background=color2, foreground=color0)
app_name.place(x=5, y=5)

# Frame_down widgets
l_name = Label(frame_down, text="Name", width=20, height=1, font="Ivy 10", background=color0, anchor=NW)
l_name.place(x=10, y=20)
entry_name = Entry(frame_down, width=25, justify="left", highlightthickness=1, relief="solid")
entry_name.insert(0, "Enter Name")  # Placeholder text
entry_name.bind("<FocusIn>", lambda event: entry_name.delete(0, END) if entry_name.get() == "Enter Name" else None)
entry_name.place(x=80, y=20)

l_gender = Label(frame_down, text="Gender", width=20, height=1, font="Ivy 10", background=color0, anchor=NW)
l_gender.place(x=10, y=50)
combo_gender = ttk.Combobox(frame_down, width=22)
combo_gender["values"] = ["", "F", "M"]
combo_gender.place(x=80, y=50)

l_telephone = Label(frame_down, text="Telephone", height=1, font="Ivy 10", background=color0, anchor=NW)
l_telephone.place(x=10, y=80)
entry_telephone = Entry(frame_down, width=25, justify="left", highlightthickness=1, relief="solid")
entry_telephone.insert(0, "Enter Telephone")  # Placeholder text
entry_telephone.bind("<FocusIn>", lambda event: entry_telephone.delete(0, END) if entry_telephone.get() == "Enter Telephone" else None)
entry_telephone.place(x=80, y=80)

l_email = Label(frame_down, text="Email", height=1, font="Ivy 10", background=color0, anchor=NW)
l_email.place(x=10, y=110)
entry_email = Entry(frame_down, width=25, justify="left", highlightthickness=1, relief="solid")
entry_email.insert(0, "Enter Email")  # Placeholder text
entry_email.bind("<FocusIn>", lambda event: entry_email.delete(0, END) if entry_email.get() == "Enter Email" else None)
entry_email.place(x=80, y=110)

placeholder_font = ("Ivy", 8)

entry_search = Entry(frame_down, width=21, justify="left", font="Ivy 11", highlightthickness=1, relief="solid")
entry_search.insert(0, "Search by Telephone")  # Placeholder text
entry_search.configure(font=placeholder_font)  # Apply smaller font to placeholder text
entry_search.bind("<FocusIn>", lambda event: entry_search.delete(0, END) if entry_search.get() == "Search by Telephone" else None)
entry_search.place(x=347, y=20)

button_search = Button(frame_down, text="Search", height=1, background=color2, foreground=color0, font="Ivy 8 bold", command=to_search)
button_search.place(x=290, y=20)

button_view = Button(frame_down, text="View", width=10, height=1, background=color2, foreground=color0, font="Ivy 8 bold", command=show)
button_view.place(x=290, y=50)

button_add = Button(frame_down, text="Add", width=10, height=1, background=color2, foreground=color0, font="Ivy 8 bold", command=insert)
button_add.place(x=400, y=50)

button_update = Button(frame_down, text="Update", width=10, height=1, background=color2, foreground=color0, font="Ivy 8 bold", command=to_update)
button_update.place(x=290, y=80)

button_delete = Button(frame_down, text="Delete", width=10, height=1, background=color2, foreground=color0, font="Ivy 8 bold", command=to_remove)
button_delete.place(x=400, y=80)

window.mainloop()