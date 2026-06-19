import tkinter as tk
from tkinter import ttk

# ==========================
# Window Setup
# ==========================
root = tk.Tk()
root.title("Agriculture Support System")
root.geometry("900x600")
root.configure(bg="#E8F5E9")

# ==========================
# FUNCTIONS
# ==========================
def clear_fields():
    farmer_id.delete(0, tk.END)
    farmer_name.delete(0, tk.END)
    crop.delete(0, tk.END)
    farm_size.delete(0, tk.END)
    location.delete(0, tk.END)

def exit_program():
    root.destroy()

def add_farmer():
    id_val = farmer_id.get()
    name_val = farmer_name.get()
    crop_val = crop.get()
    size_val = farm_size.get()
    loc_val = location.get()

    if id_val == "" or name_val == "" or crop_val == "" or size_val == "" or loc_val == "":
        status.config(text="Status: Please fill all fields")
        return

    tree.insert("", tk.END, values=(id_val, name_val, crop_val, size_val, loc_val))
    status.config(text="Status: Farmer added successfully")
    clear_fields()

def select_record(event):
    selected = tree.selection()
    if not selected:
        return

    values = tree.item(selected[0], "values")

    clear_fields()

    farmer_id.insert(0, values[0])
    farmer_name.insert(0, values[1])
    crop.insert(0, values[2])
    farm_size.insert(0, values[3])
    location.insert(0, values[4])

    status.config(text="Status: Farmer selected")

def update_farmer():
    selected = tree.selection()

    if not selected:
        status.config(text="Status: Select a farmer first")
        return

    tree.item(selected[0], values=(
        farmer_id.get(),
        farmer_name.get(),
        crop.get(),
        farm_size.get(),
        location.get()
    ))

    status.config(text="Status: Farmer updated successfully")
    clear_fields()

def delete_farmer():
    selected = tree.selection()

    if not selected:
        status.config(text="Status: Select a farmer to delete")
        return

    tree.delete(selected[0])
    status.config(text="Status: Farmer deleted successfully")
    clear_fields()

def search_farmer():
    search_id = farmer_id.get()

    if search_id == "":
        status.config(text="Status: Enter Farmer ID to search")
        return

    # SEARCH IN TABLE
    for item in tree.get_children():
        values = tree.item(item, "values")

        if values[0] == search_id:
            tree.selection_set(item)
            tree.focus(item)

            clear_fields()

            farmer_id.insert(0, values[0])
            farmer_name.insert(0, values[1])
            crop.insert(0, values[2])
            farm_size.insert(0, values[3])
            location.insert(0, values[4])

            status.config(text="Status: Farmer found in table")
            return

    # SEARCH IN FILE
    try:
        with open("farmers.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")

                if data[0] == search_id:
                    clear_fields()

                    farmer_id.insert(0, data[0])
                    farmer_name.insert(0, data[1])
                    crop.insert(0, data[2])
                    farm_size.insert(0, data[3])
                    location.insert(0, data[4])

                    status.config(text="Status: Farmer found in file")
                    return

        status.config(text="Status: Farmer not found")

    except FileNotFoundError:
        status.config(text="Status: No saved file found")

def save_data():
    with open("farmers.txt", "w") as file:
        for item in tree.get_children():
            values = tree.item(item, "values")
            file.write(",".join(values) + "\n")

    status.config(text="Status: Data saved successfully")

def load_data():
    try:
        with open("farmers.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")

                if len(data) == 5:
                    tree.insert("", tk.END, values=data)

        status.config(text="Status: Data loaded successfully")

    except FileNotFoundError:
        status.config(text="Status: No saved file found")

# ==========================
# TITLE
# ==========================
title = tk.Label(
    root,
    text="AGRICULTURE SUPPORT SYSTEM",
    bg="#2E7D32",
    fg="white",
    font=("Arial", 20, "bold"),
    pady=10
)
title.pack(fill="x")

# ==========================
# MAIN FRAME
# ==========================
main_frame = tk.Frame(root, bg="#E8F5E9")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# ==========================
# LEFT FRAME (FORM)
# ==========================
left_frame = tk.LabelFrame(
    main_frame,
    text="Farmer Information",
    bg="#E8F5E9",
    font=("Arial", 12, "bold")
)
left_frame.pack(side="left", fill="y", padx=10)

tk.Label(left_frame, text="Farmer ID:", bg="#E8F5E9").grid(row=0, column=0, sticky="w")
farmer_id = tk.Entry(left_frame)
farmer_id.grid(row=0, column=1)

tk.Label(left_frame, text="Farmer Name:", bg="#E8F5E9").grid(row=1, column=0, sticky="w")
farmer_name = tk.Entry(left_frame)
farmer_name.grid(row=1, column=1)

tk.Label(left_frame, text="Crop:", bg="#E8F5E9").grid(row=2, column=0, sticky="w")
crop = tk.Entry(left_frame)
crop.grid(row=2, column=1)

tk.Label(left_frame, text="Farm Size:", bg="#E8F5E9").grid(row=3, column=0, sticky="w")
farm_size = tk.Entry(left_frame)
farm_size.grid(row=3, column=1)

tk.Label(left_frame, text="Location:", bg="#E8F5E9").grid(row=4, column=0, sticky="w")
location = tk.Entry(left_frame)
location.grid(row=4, column=1)

# ==========================
# BUTTONS
# ==========================
button_frame = tk.Frame(left_frame, bg="#E8F5E9")
button_frame.grid(row=5, column=0, columnspan=2, pady=15)

tk.Button(button_frame, text="Add", bg="green", fg="white", width=8, command=add_farmer).grid(row=0, column=0)
tk.Button(button_frame, text="Update", bg="blue", fg="white", width=8, command=update_farmer).grid(row=0, column=1)
tk.Button(button_frame, text="Delete", bg="red", fg="white", width=8, command=delete_farmer).grid(row=0, column=2)
tk.Button(button_frame, text="Search", bg="orange", fg="white", width=8, command=search_farmer).grid(row=0, column=3)
tk.Button(button_frame, text="Clear", width=8, command=clear_fields).grid(row=0, column=4)
tk.Button(button_frame, text="Save", bg="purple", fg="white", width=8, command=save_data).grid(row=0, column=5)
tk.Button(button_frame, text="Exit", bg="black", fg="white", width=8, command=exit_program).grid(row=0, column=6)

# ==========================
# RIGHT FRAME (TABLE)
# ==========================
right_frame = tk.Frame(main_frame, bg="#E8F5E9")
right_frame.pack(side="right", fill="both", expand=True)

tree = ttk.Treeview(
    right_frame,
    columns=("id", "name", "crop", "size", "location"),
    show="headings"
)

for col in ("id", "name", "crop", "size", "location"):
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack(fill="both", expand=True)

tree.bind("<<TreeviewSelect>>", select_record)

# ==========================
# STATUS BAR
# ==========================
status = tk.Label(
    root,
    text="Status: Ready",
    bg="#2E7D32",
    fg="white",
    anchor="w"
)
status.pack(side="bottom", fill="x")

# ==========================
# LOAD DATA + RUN
# ==========================
load_data()
root.mainloop()