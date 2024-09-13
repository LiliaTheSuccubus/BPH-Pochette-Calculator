# # Define each item type with their respective slot usage and damage effects
# items = {
#     "3_slot_add_2_lines_of_2_dmg": {"slots": 3, "lines": 2, "dmg_per_line": 2},
#     "1_slot_add_2_dmg_to_all_lines": {"slots": 1, "lines": 0, "dmg_to_all_lines": 2},
#     "2_slot_add_3_dmg_to_all_lines": {"slots": 2, "lines": 0, "dmg_to_all_lines": 3},
#     "1_slot_add_1_dmg_to_all_lines": {"slots": 1, "lines": 0, "dmg_to_all_lines": 1},
#     "1_slot_add_1_line_of_1_dmg": {"slots": 1, "lines": 1, "dmg_per_line": 1}
# }

# # Input the quantity of each item type
# item_quantities = {
#     "3_slot_add_2_lines_of_2_dmg": 0,  # Replace with the number of items you want to use
#     "1_slot_add_2_dmg_to_all_lines": 0,
#     "2_slot_add_3_dmg_to_all_lines": 0,
#     "1_slot_add_1_dmg_to_all_lines": 0,
#     "1_slot_add_1_line_of_1_dmg": 0
# }

# # Function to calculate the total damage
# def calculate_damage(item_quantities):
#     total_damage = 0
#     total_lines = 0
#     total_slots_used = 0
    
#     # Calculate lines and initial damage from items that add lines
#     for item, qty in item_quantities.items():
#         item_data = items[item]
#         slots_used = item_data["slots"] * qty
#         total_slots_used += slots_used
        
#         if "lines" in item_data:
#             total_lines += item_data["lines"] * qty
#             total_damage += item_data.get("dmg_per_line", 0) * item_data["lines"] * qty

#     # Apply damage to all lines from items that add damage to all lines
#     for item, qty in item_quantities.items():
#         item_data = items[item]
#         if "dmg_to_all_lines" in item_data:
#             total_damage += item_data["dmg_to_all_lines"] * total_lines * qty

#     return total_damage, total_slots_used

# # Calculate damage
# total_damage, slots_used = calculate_damage(item_quantities)
# print(f"Total Damage: {total_damage}, Total Slots Used: {slots_used}")

# # Add logic to ensure slots don't exceed available
# available_slots = 9
# if slots_used > available_slots:
#     print("Error: Exceeded available slots.")


## above uses math to calculate, below uses arrays
###########################################################
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
initial_damage = []

# Define the initial damage array for the pet
# Example: pet1 starts with 1 line of 8 damage
# initial_damage = [8]  # Modify this array based on your pet's initial stats

# Define items with their effects on lines or damage
items = {
    "3_slot_add_2_lines_of_2_dmg": {"slots": 3, "lines": [2, 2]},  # Adds two lines of 2 damage each
    "1_slot_add_2_dmg_to_all_lines": {"slots": 1, "dmg_to_all": 2},  # Adds 2 damage to all lines
    "2_slot_add_3_dmg_to_all_lines": {"slots": 2, "dmg_to_all": 3},  # Adds 3 damage to all lines
    "1_slot_add_1_dmg_to_all_lines": {"slots": 1, "dmg_to_all": 1},  # Adds 1 damage to all lines
    "1_slot_add_1_line_of_1_dmg": {"slots": 1, "lines": [1]}         # Adds one line of 1 damage
}

# Function to parse the initial damage from the input field
def update_initial_damage():
    global initial_damage
    # Parse the input field and convert to a list of integers
    damage_input = initial_damage_entry.get()
    try:
        initial_damage = [int(x.strip()) for x in damage_input.split(',') if x.strip().isdigit()]
        result_label.configure(text=f"Initial Damage Set: {initial_damage}")
    except ValueError:
        result_label.configure(text="Enter valid numbers separated by commas.")

# Function to calculate total damage with array manipulation
def calculate_total_damage(initial_damage, items, item_quantities):
    current_damage = initial_damage[:]
    for item, qty in item_quantities.items():
        for _ in range(qty):
            if "lines" in items[item]:
                current_damage.extend(items[item]["lines"])
    for item, qty in item_quantities.items():
        for _ in range(qty):
            if "dmg_to_all" in items[item]:
                current_damage = [line + items[item]["dmg_to_all"] for line in current_damage]
    total_damage = sum(current_damage)
    return current_damage, total_damage

# Function to parse the initial damage input from the entry field
def parse_initial_damage(input_text):
    try:
        # Split the input string by commas and convert each part to an integer
        return [int(value.strip()) for value in input_text.split(',') if value.strip()]
    except ValueError:
        # Return an empty list if parsing fails
        result_label.configure(text="Enter valid numbers separated by commas.")
        return []

# Function to handle adding item quantities and setting initial damage from the GUI
def add_item():
    global initial_damage
    # Check if the initial damage field is not empty
    damage_input = initial_damage_entry.get().strip()
    if damage_input:
        try:
            # Parse the input field and convert to a list of integers
            initial_damage = [int(x.strip()) for x in damage_input.split(',') if x.strip().isdigit()]
            result_label.configure(text=f"Initial Damage Set: {initial_damage}")
            initial_damage_entry.delete(0, tk.END)  # Clear the field after setting initial damage
            return  # Return after setting initial damage to avoid running the item addition
        except ValueError:
            result_label.configure(text="Enter valid numbers separated by commas.")
            return
    
    # Check if initial damage array is empty
    if not initial_damage:
        result_label.configure(text="Initial damage cannot be empty.")
        return

    # Continue with adding item quantities if initial damage is already set
    selected_item = item_combobox.get()
    try:
        quantity = int(quantity_entry.get())
        item_quantities[selected_item] = quantity
    except ValueError:
        result_label.configure(text="Enter a valid number for quantity.")
        return

    damage_array, total_damage = calculate_total_damage(initial_damage, items, item_quantities)
    result_label.configure(text=f"Damage Array: {damage_array}\nTotal Damage: {total_damage}")

# Create the main application window
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.iconbitmap("1.ico")
root.geometry("420x200")
root.attributes('-topmost', 1)
root.title("Backpack Hero Pochette Pet Calculator")
global_padding = 5

def create_label(text, row, column, columnspan=1, padx=global_padding, pady=0, sticky=None):
    label = ctk.CTkLabel(root, text=text, bg_color="#242424")
    label.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady, sticky=sticky)
    return label

def create_button(text, command, row, column, width=5, columnspan=1, padx=global_padding, pady=0, sticky=None):
    button = ctk.CTkButton(root, text=text, command=command, fg_color=("#1C1C1C", "#1C1C1C"), hover_color=("#424242", "#424242"), width=width)
    button.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady, sticky=sticky)
    return button

def create_combobox(values, row, column, event_handler=None, sticky=None):
    width = len(max(values, key=len)) if values else 3
    combobox = ttk.Combobox(root, values=values if values else [""], width=width)
    combobox.grid(row=row, column=column, sticky=sticky)
    if event_handler:
        combobox.bind('<<ComboboxSelected>>', lambda event: event_handler())
    return combobox

# Dropdown for item selection
create_label("Select Item:", 0, 0)
item_combobox = create_combobox(list(items.keys()), 0, 1)
# consolidated below lines into single function above
# item_label = tk.Label(root, text="Select Item:")
# item_label.grid(row=0, column=0, padx=5, pady=5)
# item_combobox = ttk.Combobox(root, values=list(items.keys()))
# item_combobox.grid(row=0, column=1, padx=5, pady=5)
# item_combobox.set("Select an item")

create_label("Initial Damage (comma-separated):", 1, 0)
initial_damage_entry = ctk.CTkEntry(root)
initial_damage_entry.grid(row=1, column=1, padx=5, pady=5)

# Entry field for quantity input
create_label("Enter Quantity:", 2, 0)
quantity_entry = ctk.CTkEntry(root)
quantity_entry.grid(row=2, column=1, padx=5, pady=5)
# quantity_label = tk.Label(root, text="Enter Quantity:")
# quantity_label.grid(row=2, column=0, padx=5, pady=5)

# Button to add the item and calculate damage
create_button("Add Item", add_item, 3, 0, 5, 2, 5, 10)
# add_button = tk.Button(root, text="Add Item", command=add_item)
# add_button.grid(row=3, column=0, columnspan=2, pady=10)

# Label to display the result
result_label = create_label("", 4, 0, 2, 5, 10)
# result_label = tk.Label(root, text="")
# result_label.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

# Dictionary to hold quantities
item_quantities = {key: 0 for key in items.keys()}

root.mainloop()