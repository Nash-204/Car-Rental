import tkinter as tk
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkImage, set_appearance_mode, CTkEntry, \
    CTkScrollableFrame, CTkRadioButton
from PIL import Image, ImageTk
import datetime

selected_car = None
saved_bookings = []  # List to store saved bookings

# Function to set appearance mode to dark
def dark_appearance_mode():
    set_appearance_mode("dark")
    image_label.config(bg="darkgray")


# Function to set appearance mode to light
def light_appearance_mode():
    set_appearance_mode("light")
    image_label.config(bg="white")


# Function to switch to car selection view
def show_cars():
    # Hide the booking frame
    Booking_Frame.pack_forget()
    Reservation_Frame.pack_forget()
    image_frame.pack_forget()
    Payment_Frame.pack_forget()
    # Show the car frame
    Cars_Frame.pack(side="right", fill="both", padx=0, pady=0, expand=True)


# Function to switch to booking view
def show_booking():
    # Show the booking frame
    Cars_Frame.pack_forget()  # Hide the cars frame
    image_frame.pack_forget()
    Reservation_Frame.pack_forget()
    Payment_Frame.pack_forget()
    Booking_Frame.pack(side="right", fill="both", padx=0, pady=0, expand=True)
    if selected_car:
        selected_car_label.configure(text=f"Selected Car: {selected_car}")
    else:
        selected_car_label.configure(text="No car selected")


# Function to handle button clicks
def select_car(car_name):
    global selected_car
    selected_car = car_name
    print("Selected car:", selected_car)


# Function to save the booking
def save_booking():
    global selected_car  # Declare selected_car as global
    name = name_entry.get()
    date = date_entry.get()
    duration = duration_entry.get()

    # Error trapping for name entry (allow only letters)
    if not name.isalpha():
        command_prompt.configure(text="Name should contain only letters.")
        return

    # Error trapping for date entry (allow only dates more than the current date)
    try:
        parsed_date = datetime.datetime.strptime(date, "%m-%d-%Y")
        current_date = datetime.datetime.now()
        if parsed_date <= current_date:
            command_prompt.configure(text="Please select a date after the current date.")
            return
    except ValueError:
        command_prompt.configure(text="Invalid date format. Please use MM-DD-YYYY.")
        return

    # Error trapping for duration entry (allow only integers)
    try:
        duration = int(duration)
    except ValueError:
        command_prompt.configure(text="Duration should be a valid integer.")
        return

    # Check if all fields are filled and a car is selected
    if name and date and duration and selected_car:
        booking_info = {"Name": name, "Date": date, "Duration": duration, "Car": selected_car}
        saved_bookings.append(booking_info)
        print("Booking saved!")
        # Update the reservations table
        update_reservation_table()
        # Clear the entry fields
        name_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        duration_entry.delete(0, tk.END)
        # Reset selected car
        selected_car = None
        # Show success message
        command_prompt.configure(text="Booking saved successfully!")
    else:
        print("Please fill in all the fields and select a car.")
        # Show error message
        command_prompt.configure(text="Please fill in all the fields and select a car.")


# Function to update the reservations table
def update_reservation_table():
    # Clear existing rows in the table
    for widget in reservation_table.grid_slaves():
        widget.grid_forget()

    # Create headers
    CTkLabel(master=frame, text="#", font=("Arial", 12, "bold"), width=10).grid(row=0, column=0, padx=5, pady=5)
    CTkLabel(master=frame, text="Car", font=("Arial", 12, "bold"), width=100).grid(row=0, column=1, padx=5, pady=5)
    CTkLabel(master=frame, text="Name", font=("Arial", 12, "bold"), width=100).grid(row=0, column=2, padx=5, pady=5)
    CTkLabel(master=frame, text="Date", font=("Arial", 12, "bold"), width=100).grid(row=0, column=3, padx=5, pady=5)
    CTkLabel(master=frame, text="Duration", font=("Arial", 12, "bold"), width=100).grid(row=0, column=4, padx=5, pady=5)
    CTkLabel(master=frame, text="Edit", font=("Arial", 12, "bold"), width=100).grid(row=0, column=5, padx=5, pady=5)
    CTkLabel(master=frame, text="Delete", font=("Arial", 12, "bold"), width=100).grid(row=0, column=6, padx=5, pady=5)

    # Populate with saved bookings
    for i, booking in enumerate(saved_bookings, start=1):
        # Display booking information
        CTkLabel(master=frame, text=str(i), font=("Arial", 12), width=10).grid(row=i, column=0, padx=5, pady=5)
        CTkLabel(master=frame, text=booking["Car"], font=("Arial", 12), width=100).grid(row=i, column=1, padx=5, pady=5)
        CTkLabel(master=frame, text=booking["Name"], font=("Arial", 12), width=100).grid(row=i, column=2, padx=5,
                                                                                         pady=5)
        CTkLabel(master=frame, text=booking["Date"], font=("Arial", 12), width=100).grid(row=i, column=3, padx=5,
                                                                                         pady=5)
        CTkLabel(master=frame, text=booking["Duration"], font=("Arial", 12), width=100).grid(row=i, column=4, padx=5,
                                                                                             pady=5)

        # Create edit button for each row
        edit_button = CTkButton(master=frame, text="Edit", command=lambda idx=i: edit_booking(idx), width=80)
        edit_button.grid(row=i, column=5, padx=2, pady=2)

        # Create delete button for each row
        delete_button = CTkButton(master=frame, text="Delete", command=lambda idx=i: delete_booking(idx), width=80)
        delete_button.grid(row=i, column=6, padx=2, pady=2)


def edit_booking(row_index):
    # Get the booking to edit
    booking_to_edit = saved_bookings[row_index - 1]  # Adjust for 1-based indexing

    # Create a popup window for editing
    edit_window = tk.Toplevel()
    edit_window.title("Edit Booking")

    # Label and Entry for user's name
    name_label = CTkLabel(master=edit_window, text="Enter your name:", font=("Arial", 14))
    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry = CTkEntry(master=edit_window, placeholder_text="Start typing...", width=300)
    name_entry.insert(0, booking_to_edit["Name"])  # Populate with existing data
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    # Label and Entry for rental date
    date_label = CTkLabel(master=edit_window, text="Rental date (MM-DD-YYYY):", font=("Arial", 14))
    date_label.grid(row=1, column=0, padx=5, pady=5)
    date_entry = CTkEntry(master=edit_window, placeholder_text="Start typing...", width=300)
    date_entry.insert(0, booking_to_edit["Date"])  # Populate with existing data
    date_entry.grid(row=1, column=1, padx=5, pady=5)

    # Label and Entry for rental duration
    duration_label = CTkLabel(master=edit_window, text="Rental duration (days):", font=("Arial", 14))
    duration_label.grid(row=2, column=0, padx=5, pady=5)
    duration_entry = CTkEntry(master=edit_window, placeholder_text="Start typing...", width=300)
    duration_entry.insert(0, booking_to_edit["Duration"])  # Populate with existing data
    duration_entry.grid(row=2, column=1, padx=5, pady=5)

    # Update the cars list with price for each car
    cars = [
        {"name": "Sedan", "price": "1,500", "image": "Sedan.png"},
        {"name": "Hatchback", "price": "1,000", "image": "Hatchback.png"},
        {"name": "Convertible", "price": "2,000", "image": "Convertable.png"},
        {"name": "Pickup", "price": "2,500", "image": "Pickup.png"},
        {"name": "SUV", "price": "3,000", "image": "SUV.png"},
        {"name": "Van", "price": "3,500", "image": "Van.png"}
    ]

    selected_car_label = CTkLabel(master=edit_window, text="Select Car:", font=("Arial", 14))
    selected_car_label.grid(row=3, column=0, padx=5, pady=5)

    # Set a fixed size for car buttons
    button_width = 205
    button_height = 250

    # Function to update the selected car
    def update_selected_car(car_name):
        global selected_car
        selected_car = car_name

    # Iterate through the list of cars to create buttons
    for i, car in enumerate(cars):
        # Open the image file and resize it
        car_image = Image.open(car["image"])

        # Convert the resized image to CTkImage
        ctk_car_image = CTkImage(light_image=car_image, size=(150, 150))

        # Create a CTkButton with the car name and CTkImage
        car_button = CTkButton(master=edit_window, text=f"{car['name']} (₱{car['price']}/day)", image=ctk_car_image,
                               compound="top",
                               command=lambda c=car["name"]: select_car(c))

        # Keep a reference to the CTkImage to prevent garbage collection
        car_button.image = ctk_car_image

        # Spread out the buttons within the grid
        car_button.grid(row=(i // 3) + 4, column=i % 3, padx=10, pady=10, sticky="nsew")

    # Create a button to save the edited booking
    save_button = CTkButton(master=edit_window, text="Save",
                            command=lambda: save_edited_booking(row_index, name_entry.get(),
                                                                date_entry.get(), duration_entry.get(), edit_window))
    save_button.grid(row=7, column=0, columnspan=2, pady=20)


def save_edited_booking(row_index, name, date, duration, window):
    # Check if all fields are filled
    if name and date and duration:
        # Update the booking information
        saved_bookings[row_index - 1] = {"Car": selected_car, "Name": name, "Date": date, "Duration": duration}
        # Update the reservations table
        update_reservation_table()
        window.destroy()
    else:
        # Show error message if any field is empty
        command_prompt.configure(text="Please fill in all the fields.")


def delete_booking(row_index):
    # Remove the booking from saved bookings list
    saved_bookings.pop(row_index - 1)  # Adjust for 1-based indexing
    # Update the reservations table
    update_reservation_table()


# Function to show the reservations
def show_reservations():
    Cars_Frame.pack_forget()  # Hide the cars frame
    image_frame.pack_forget()
    Booking_Frame.pack_forget()
    Payment_Frame.pack_forget()
    Reservation_Frame.pack(side="right", fill="both", padx=0, pady=0, expand=True)
    # Update the reservations table
    update_reservation_table()


def show_payment():
    Cars_Frame.pack_forget()  # Hide the cars frame
    image_frame.pack_forget()
    Booking_Frame.pack_forget()
    Reservation_Frame.pack_forget()
    Payment_Frame.pack(side="right", fill="both", padx=0, pady=0, expand=True)


# Create the main tkinter window
app = tk.Tk()
app.geometry("900x600")
app.title("Car Rental System")
app.resizable(False, False)

# Set initial appearance mode to light
set_appearance_mode("light")

# Load the image with a transparent background
image = Image.open("Car Rental.png")
image = image.resize((400, 250))  # Resize the image to fit the window
photo = ImageTk.PhotoImage(image)

# Create a frame for the image
image_frame = tk.Frame(app)
image_frame.pack(side="right", fill="both", expand=True)

# Display the image
image_label = tk.Label(image_frame, image=photo)
image_label.image = photo  # Keep a reference to prevent garbage collection
image_label.pack(fill="both", expand=True)

# Create a frame for buttons using customtkinter
frame_1 = CTkFrame(master=app)
frame_1.pack(side="left", fill="y")  # Use pack to fill both directions
CTkLabel(master=frame_1, text="CarToGO", font=("Arial Bold", 25)).grid(row=0, column=0, columnspan=2, pady=[30, 20])

# Create buttons for light and dark modes
dark_button = CTkButton(master=frame_1, text="Dark Mode", command=dark_appearance_mode, width=10)
dark_button.grid(row=1, column=0, padx=5, pady=5)

light_button = CTkButton(master=frame_1, text="Light Mode", command=light_appearance_mode, width=10)
light_button.grid(row=1, column=1, padx=5, pady=5)

# Create a button for selecting cars
cars_button = CTkButton(master=frame_1, text="Cars", command=show_cars, width=10)
cars_button.grid(row=2, column=0, columnspan=2, pady=(30, 15), padx=30, sticky="ew")

# Create a frame for cars
Cars_Frame = CTkFrame(master=app)

# Create buttons for selecting cars
cars = [
    {"name": "Sedan", "price": "1,500", "image": "Sedan.png"},
    {"name": "Hatchback", "price": "1,000", "image": "Hatchback.png"},
    {"name": "Convertible", "price": "2,000", "image": "Convertable.png"},
    {"name": "Pickup", "price": "2,500", "image": "Pickup.png"},
    {"name": "SUV", "price": "3,000", "image": "SUV.png"},
    {"name": "Van", "price": "3,500", "image": "Van.png"}
]

# Iterate through the list of cars to create buttons
for i, car in enumerate(cars):
    # Open the image file and resize it
    car_image = Image.open(car["image"])

    # Convert the resized image to CTkImage
    ctk_car_image = CTkImage(light_image=car_image, size=(205, 250))

    # Create a CTkButton with the car name and price
    car_button = CTkButton(master=Cars_Frame, text=f"{car['name']} (₱{car['price']}/day)", image=ctk_car_image, compound="top",
                           command=lambda c=car["name"]: select_car(c))

    # Keep a reference to the CTkImage to prevent garbage collection
    car_button.image = ctk_car_image

    # Spread out the buttons within the grid
    car_button.grid(row=i // 3, column=i % 3, padx=10, pady=10, sticky="nsew")

# Create a button for booking
booking_button = CTkButton(master=frame_1, text="Booking", command=show_booking, width=10)
booking_button.grid(row=3, column=0, columnspan=2, pady=(30, 15), padx=30, sticky="ew")

# Create a frame for booking
Booking_Frame = CTkFrame(master=app)

# Create a label for the booking section
CTkLabel(master=Booking_Frame, text="Booking Section", font=("Arial Bold", 25)).pack(pady=[30, 20])

# Label to display selected car
selected_car_label = CTkLabel(master=Booking_Frame, text="", font=("Arial", 16, "bold"))
selected_car_label.pack(pady=10)

# Label and Entry for user's name
name_label = CTkLabel(master=Booking_Frame, text="Enter your name:", font=("Arial", 14))
name_label.pack(pady=5)
name_entry = CTkEntry(master=Booking_Frame, placeholder_text="Start typing...", width=300)
name_entry.pack(pady=5)

# Label and Entry for rental date
date_label = CTkLabel(master=Booking_Frame, text="Rental date (MM-DD-YYYY):", font=("Arial", 14))
date_label.pack(pady=5)
date_entry = CTkEntry(master=Booking_Frame, placeholder_text="Start typing...", width=300)
date_entry.pack(pady=5)

# Label and Entry for rental duration
duration_label = CTkLabel(master=Booking_Frame, text="Rental duration (days):", font=("Arial", 14))
duration_label.pack(pady=5)
duration_entry = CTkEntry(master=Booking_Frame, placeholder_text="Start typing...", width=300)
duration_entry.pack(pady=5)

# Create a "Save" button to save the booking
save_button = CTkButton(master=Booking_Frame, text="Save", command=save_booking, width=10)
save_button.pack(pady=20)


# Create a command prompt label
command_prompt = CTkLabel(master=Booking_Frame, text="", font=("Arial", 12))
command_prompt.pack(pady=10)

# Create a button for new reservations
reservation_button = CTkButton(master=frame_1, text="Reservations", command=show_reservations, width=15)
reservation_button.grid(row=4, column=0, columnspan=2, pady=(30, 15), padx=30, sticky="ew")

# Create a frame for booking
Reservation_Frame = CTkFrame(master=app)
# Create a label for the booking section
CTkLabel(master=Reservation_Frame, text="Reservations Section", font=("Arial Bold", 25)).pack(pady=[30, 20])
# Create the CTkScrollableFrame
frame = CTkScrollableFrame(master=Reservation_Frame, border_width=5, orientation="vertical")
frame.pack(expand=True, fill="both")
# Use the frame itself as the reservation table
reservation_table = frame


# Create a button for payment
payment_button = CTkButton(master=frame_1, text="Payment", command=show_payment, width=15)
payment_button.grid(row=5, column=0, columnspan=2, pady=(30, 15), padx=30, sticky="ew")

# Create a frame for payment
Payment_Frame = CTkFrame(master=app)
# Create a label for the payment section
CTkLabel(master=Payment_Frame, text="Payment Section", font=("Arial Bold", 25)).pack(pady=[30, 20])

# Label and Entry for reservation number
reservation_label = CTkLabel(master=Payment_Frame, text="Enter your reservation number:", font=("Arial", 14))
reservation_label.pack(pady=5)
reservation_entry = CTkEntry(master=Payment_Frame, placeholder_text="Enter reservation number", width=300)
reservation_entry.pack(pady=5)


# Function to handle payment
def process_payment():
    reservation_number = reservation_entry.get()

    # Check if the reservation number is valid
    try:
        reservation_index = int(reservation_number) - 1  # Adjust for 1-based indexing
        booking_info = saved_bookings[reservation_index]
        car_name = booking_info["Car"]
        duration = booking_info["Duration"]

        # Retrieve the price of the selected car
        car_price = next(car["price"] for car in cars if car["name"] == car_name)

        # Calculate total price
        total_price = int(car_price.replace(",", "")) * duration

        # Display the computed price to the user
        price_label.configure(text=f"Total Price: ₱{total_price}")

        # Get the selected payment method
        payment_method = payment_var.get()

        # Process the payment based on the selected method
        if payment_method == "Cash":
            # Handle cash payment
            # Display success message
            payment_prompt.configure(text="Payment successful! Thank you for your purchase.")
        elif payment_method == "Card":
            # Handle card payment
            # Display success message
            payment_prompt.configure(text="Payment successful! Thank you for your purchase.")
        elif payment_method == "Emoney":
            # Handle Emoney payment
            # Display success message
            payment_prompt.configure(text="Payment successful! Thank you for your purchase.")
        else:
            # Display error message if no payment method selected
            payment_prompt.configure(text="Please select a payment method.")
    except (ValueError, IndexError):
        # Display error message for invalid reservation number
        payment_prompt.configure(text="Invalid reservation number.")


# Radio buttons for payment method
payment_var = tk.StringVar(value="Cash")  # Default to Cash
cash_radio = CTkRadioButton(master=Payment_Frame, text="Cash", variable=payment_var, value="Cash")
cash_radio.pack(pady=5)
card_radio = CTkRadioButton(master=Payment_Frame, text="Card", variable=payment_var, value="Card")
card_radio.pack(pady=5)
emoney_radio = CTkRadioButton(master=Payment_Frame, text="Emoney", variable=payment_var, value="Emoney")
emoney_radio.pack(pady=5)

# Button to process payment
payment_button = CTkButton(master=Payment_Frame, text="Save", command=process_payment, width=10)
payment_button.pack(pady=20)

# Label to display the computed price
price_label = CTkLabel(master=Payment_Frame, text="", font=("Arial", 14))
price_label.pack(pady=10)

# Label to display payment prompt
payment_prompt = CTkLabel(master=Payment_Frame, text="", font=("Arial", 12))
payment_prompt.pack(pady=10)

# Start with Cars_Frame and Booking_Frame hidden
Cars_Frame.pack_forget()
Booking_Frame.pack_forget()
Reservation_Frame.pack_forget()
Payment_Frame.pack_forget()

# Start the Tkinter event loop
app.mainloop()
