
import customtkinter as ctk
from tkinter import messagebox
import sqlite3

ctk.set_appearance_mode("darkblue")
ctk.set_default_color_theme("green")

conn = sqlite3.connect("contacts.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    address TEXT
)
""")
conn.commit()

class ContactBookApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("📒 Contact Book")
        self.geometry("800x600")
        self.resizable(False, False)

        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y", padx=5, pady=5)

        ctk.CTkLabel(self.sidebar, text="📁 Menu", font=("Arial", 20)).pack(pady=10)

        ctk.CTkButton(self.sidebar, text="➕ Add Contact", command=self.load_add_view).pack(pady=10)
        ctk.CTkButton(self.sidebar, text="📋 View Contacts", command=self.load_list_view).pack(pady=10)
        ctk.CTkButton(self.sidebar, text="🔍 Search Contact", command=self.load_search_view).pack(pady=10)
        ctk.CTkButton(self.sidebar, text="❌ Exit", command=self.destroy).pack(pady=10)

        self.content = ctk.CTkFrame(self)
        self.content.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        self.load_add_view()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def load_add_view(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Add New Contact", font=("Arial", 24)).pack(pady=20)

        self.name_entry = ctk.CTkEntry(self.content, placeholder_text="Full Name")
        self.name_entry.pack(pady=5)
        self.phone_entry = ctk.CTkEntry(self.content, placeholder_text="Phone Number")
        self.phone_entry.pack(pady=5)
        self.email_entry = ctk.CTkEntry(self.content, placeholder_text="Email")
        self.email_entry.pack(pady=5)
        self.address_entry = ctk.CTkEntry(self.content, placeholder_text="Address")
        self.address_entry.pack(pady=5)

        ctk.CTkButton(self.content, text="💾 Save Contact", command=self.add_contact).pack(pady=10)

    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()

        if not name or not phone:
            messagebox.showerror("Error", "Name and phone are required!")
            return

        cursor.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                       (name, phone, email, address))
        conn.commit()

        messagebox.showinfo("Success", "Contact added successfully!")
        self.load_add_view()

    def load_list_view(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Contact List", font=("Arial", 24)).pack(pady=10)

        cursor.execute("SELECT * FROM contacts")
        records = cursor.fetchall()

        for record in records:
            frame = ctk.CTkFrame(self.content)
            frame.pack(fill="x", padx=10, pady=5)

            label_text = f"{record[1]} - {record[2]}"
            ctk.CTkLabel(frame, text=label_text, anchor="w").pack(side="left", fill="x", expand=True)

            ctk.CTkButton(frame, text="✏️", width=40, command=lambda rid=record[0]: self.load_edit_view(rid)).pack(side="right", padx=3)
            ctk.CTkButton(frame, text="🗑️", width=40, command=lambda rid=record[0]: self.delete_contact(rid)).pack(side="right", padx=3)

    def load_edit_view(self, record_id):
        self.clear_content()
        cursor.execute("SELECT * FROM contacts WHERE id=?", (record_id,))
        record = cursor.fetchone()

        ctk.CTkLabel(self.content, text="Edit Contact", font=("Arial", 24)).pack(pady=20)

        self.name_entry = ctk.CTkEntry(self.content)
        self.name_entry.insert(0, record[1])
        self.name_entry.pack(pady=5)

        self.phone_entry = ctk.CTkEntry(self.content)
        self.phone_entry.insert(0, record[2])
        self.phone_entry.pack(pady=5)

        self.email_entry = ctk.CTkEntry(self.content)
        self.email_entry.insert(0, record[3])
        self.email_entry.pack(pady=5)

        self.address_entry = ctk.CTkEntry(self.content)
        self.address_entry.insert(0, record[4])
        self.address_entry.pack(pady=5)

        ctk.CTkButton(self.content, text="🔄 Update Contact",
                      command=lambda rid=record[0]: self.update_contact(rid)).pack(pady=10)

    def update_contact(self, record_id):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()

        cursor.execute("UPDATE contacts SET name=?, phone=?, email=?, address=? WHERE id=?",
                       (name, phone, email, address, record_id))
        conn.commit()

        messagebox.showinfo("Success", "Contact updated!")
        self.load_list_view()

    def delete_contact(self, record_id):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this contact?"):
            cursor.execute("DELETE FROM contacts WHERE id=?", (record_id,))
            conn.commit()
            self.load_list_view()

    def load_search_view(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Search Contact", font=("Arial", 24)).pack(pady=10)

        self.search_entry = ctk.CTkEntry(self.content, placeholder_text="Enter name or phone")
        self.search_entry.pack(pady=5)

        ctk.CTkButton(self.content, text="🔍 Search", command=self.perform_search).pack(pady=5)
        self.results_frame = ctk.CTkFrame(self.content)
        self.results_frame.pack(pady=10, fill="both", expand=True)

    def perform_search(self):
        query = "%" + self.search_entry.get().strip() + "%"
        cursor.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?", (query, query))
        results = cursor.fetchall()

        for widget in self.results_frame.winfo_children():
            widget.destroy()

        if not results:
            ctk.CTkLabel(self.results_frame, text="No contacts found.").pack()
        else:
            for record in results:
                text = f"{record[1]} - {record[2]}"
                ctk.CTkLabel(self.results_frame, text=text, anchor="w").pack(pady=2)

if __name__ == "__main__":
    app = ContactBookApp()
    app.mainloop()
    conn.close()
