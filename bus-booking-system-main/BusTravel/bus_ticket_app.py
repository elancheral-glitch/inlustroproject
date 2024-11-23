import tkinter as tk
from tkinter import messagebox
import os
import subprocess
from datetime import datetime
import csv

# AdminLoginApp Class
class AdminLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Login")
        self.root.geometry("400x300")
        self.root.config(bg="#f0f0f0")

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Title label
        self.title_label = tk.Label(self.root, text="Admin Login", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        self.title_label.pack(pady=20)

        # Username label and entry
        self.username_label = tk.Label(self.root, text="Username:", font=("Arial", 12), bg="#f0f0f0")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root, font=("Arial", 12), width=30, bd=2, relief="solid")
        self.username_entry.pack(pady=5)

        # Password label and entry
        self.password_label = tk.Label(self.root, text="Password:", font=("Arial", 12), bg="#f0f0f0")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, font=("Arial", 12), width=30, bd=2, relief="solid", show="*")
        self.password_entry.pack(pady=5)

        # Login button
        self.login_button = tk.Button(self.root, text="Login", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=self.login, relief="flat", width=20, height=2)
        self.login_button.pack(pady=20)

    def login(self):
        """Login validation for admin"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Admin credentials (for this example, we hardcode it)
        admin_username = "dhanush"
        admin_password = "oviya"

        # Check if the entered credentials match the admin credentials
        if username == admin_username and password == admin_password:
            messagebox.showinfo("Success", "Login Successful!")
            self.root.quit()  # Close login window
            self.open_ticket_booking_app()  # Open the ticket booking app
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    def open_ticket_booking_app(self):
        """Open the bus ticket booking application"""
        # Open the BusTicketApp GUI
        root = tk.Tk()
        app = BusTicketApp(root)
        root.mainloop()

# BusTicketApp Class
class BusTicketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bus Ticket App")
        self.root.geometry("700x600")
        
        # Set window background color
        self.root.config(bg="#f0f0f0")

        # Create widgets with styles
        self.create_widgets()

        # Load tickets from CSV
        self.tickets = []
        self.load_tickets_from_file()

    def create_widgets(self):
        # Title label with styling
        self.title_label = tk.Label(self.root, text="Bus Ticket Registration", font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#333")
        self.title_label.pack(pady=20)

        # Passenger Name label and entry
        self.passenger_name_label = tk.Label(self.root, text="Passenger Name:", font=("Arial", 12), bg="#f0f0f0")
        self.passenger_name_label.pack()
        self.passenger_name_entry = tk.Entry(self.root, font=("Arial", 12), width=30, bd=2, relief="solid")
        self.passenger_name_entry.pack(pady=5)

        # Bus Number label and entry
        self.bus_number_label = tk.Label(self.root, text="Bus Number (e.g., B123):", font=("Arial", 12), bg="#f0f0f0")
        self.bus_number_label.pack()
        self.bus_number_entry = tk.Entry(self.root, font=("Arial", 12), width=30, bd=2, relief="solid")
        self.bus_number_entry.pack(pady=5)

        # Departure Time label and entry
        self.departure_time_label = tk.Label(self.root, text="Departure Time (YYYY-MM-DD HH:MM):", font=("Arial", 12), bg="#f0f0f0")
        self.departure_time_label.pack()
        self.departure_time_entry = tk.Entry(self.root, font=("Arial", 12), width=30, bd=2, relief="solid")
        self.departure_time_entry.pack(pady=5)

        # Origin label and entry
        self.origin_label = tk.Label(self.root, text="Origin:", font=("Arial", 12), bg="#f0f0f0")
        self.origin_label.pack()
        self.origin_entry = tk.Entry(self.root, font=("Arial", 12), width=30, bd=2, relief="solid")
        self.origin_entry.pack(pady=5)

        # Destination label and entry
        self.destination_label = tk.Label(self.root, text="Destination:", font=("Arial", 12), bg="#f0f0f0")
        self.destination_label.pack()
        self.destination_entry = tk.Entry(self.root, font=("Arial", 12), width=30, bd=2, relief="solid")
        self.destination_entry.pack(pady=5)

        # Price label and entry
        self.price_label = tk.Label(self.root, text="Ticket Price ($):", font=("Arial", 12), bg="#f0f0f0")
        self.price_label.pack()
        self.price_entry = tk.Entry(self.root, font=("Arial", 12), width=30, bd=2, relief="solid")
        self.price_entry.pack(pady=5)

        # Buttons
        button_font = ("Arial", 12, "bold")
        self.add_ticket_button = self.create_button(self.root, "Add Ticket", "#4CAF50", self.add_ticket)
        self.add_ticket_button.pack(pady=10)

        self.search_ticket_button = self.create_button(self.root, "Search Ticket", "#2196F3", self.search_ticket)
        self.search_ticket_button.pack(pady=5)

        self.show_all_button = self.create_button(self.root, "Show All Tickets", "#FF9800", self.show_all_tickets)
        self.show_all_button.pack(pady=5)

        # Ticket Listbox with Scrollbar
        self.ticket_listbox = tk.Listbox(self.root, font=("Arial", 12), width=50, height=10, bd=2, relief="solid")
        self.ticket_listbox.pack(pady=10)

        # Scrollbar for the listbox
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.ticket_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.ticket_listbox.config(yscrollcommand=self.scrollbar.set)

    def create_button(self, parent, text, bg_color, command):
        """Create a button with hover effects"""
        button = tk.Button(parent, text=text, font=("Arial", 12, "bold"), bg=bg_color, fg="white", command=command, relief="flat", width=20, height=2)
        button.bind("<Enter>", lambda event: self.on_button_hover(event, button))
        button.bind("<Leave>", lambda event: self.on_button_leave(event, button))
        return button

    def on_button_hover(self, event, button):
        """Change the button color on hover"""
        button.config(bg=self.darken_color(button.cget("bg"), 0.2))

    def on_button_leave(self, event, button):
        """Restore the original button color on leave"""
        button.config(bg=self.darken_color(button.cget("bg"), -0.2))

    def darken_color(self, color, factor):
        """Darken or lighten a color by a factor"""
        color = color.lstrip("#")
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        r = max(0, min(255, int(r + (factor * 50)) ))
        g = max(0, min(255, int(g + (factor * 50)) ))
        b = max(0, min(255, int(b + (factor * 50)) ))
        return f"#{r:02x}{g:02x}{b:02x}"

    def generate_ticket_id(self):
        return f"TK{int(datetime.now().timestamp())}"

    def load_tickets_from_file(self):
        """Load existing tickets from a CSV file"""
        try:
            with open('tickets.csv', 'r', newline='') as file:
                reader = csv.DictReader(file)
                self.tickets = [ticket for ticket in reader]
        except FileNotFoundError:
            self.tickets = []

    def save_tickets_to_file(self):
        """Save all tickets to a CSV file"""
        with open('tickets.csv', 'w', newline='') as file:
            fieldnames = ['Ticket ID', 'Passenger Name', 'Bus Number', 'Departure Time', 'Origin', 'Destination', 'Price']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.tickets)

    def add_ticket(self):
        """Add a new ticket to the list"""
        passenger_name = self.passenger_name_entry.get()
        bus_number = self.bus_number_entry.get()
        departure_time = self.departure_time_entry.get()
        origin = self.origin_entry.get()
        destination = self.destination_entry.get()
        price = self.price_entry.get()

        if not passenger_name or not bus_number or not departure_time or not origin or not destination or not price:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        ticket = {
            'Ticket ID': self.generate_ticket_id(),
            'Passenger Name': passenger_name,
            'Bus Number': bus_number,
            'Departure Time': departure_time,
            'Origin': origin,
            'Destination': destination,
            'Price': float(price)
        }

        self.tickets.append(ticket)
        self.save_tickets_to_file()

        self.clear_entries()
        messagebox.showinfo("Success", "Ticket Added Successfully!")
        self.show_all_tickets()

    def clear_entries(self):
        """Clear the entry fields after adding a ticket"""
        self.passenger_name_entry.delete(0, tk.END)
        self.bus_number_entry.delete(0, tk.END)
        self.departure_time_entry.delete(0, tk.END)
        self.origin_entry.delete(0, tk.END)
        self.destination_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

    def search_ticket(self):
        """Search tickets by Ticket ID or Passenger Name"""
        search_term = self.passenger_name_entry.get()
        if not search_term:
            messagebox.showerror("Error", "Please enter a passenger name to search.")
            return

        found_tickets = [ticket for ticket in self.tickets if search_term.lower() in ticket['Passenger Name'].lower()]

        if not found_tickets:
            messagebox.showinfo("No Results", "No tickets found.")
            return

        self.ticket_listbox.delete(0, tk.END)
        for ticket in found_tickets:
            self.ticket_listbox.insert(tk.END, f"{ticket['Ticket ID']} - {ticket['Passenger Name']}")

    def show_all_tickets(self):
        """Display all tickets in the listbox"""
        self.ticket_listbox.delete(0, tk.END)
        for ticket in self.tickets:
            self.ticket_listbox.insert(tk.END, f"{ticket['Ticket ID']} - {ticket['Passenger Name']}")

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = AdminLoginApp(root)
    root.mainloop()
