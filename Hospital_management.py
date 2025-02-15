import sqlite3

# Function to create a database connection
def create_connection():
    try:
        connection = sqlite3.connect("hospital_management.db")  # Creates a local SQLite database
        return connection
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return None

# Function to create required tables in the database
def create_tables(connection):
    cursor = connection.cursor()
    
    # Create Patients Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT CHECK(gender IN ('Male', 'Female', 'Other')),
        contact_number TEXT UNIQUE,
        address TEXT
    )
    """)
    
    # Create Bills Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bills (
        bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        bill_amount REAL CHECK(bill_amount > 0),
        payment_status TEXT CHECK(payment_status IN ('Pending', 'Paid')),
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
    )
    """)
    
    connection.commit()

# Function to add a new patient record
def add_patient(connection):
    name = input("Enter patient name: ")
    age = int(input("Enter age: "))
    gender = input("Enter gender (Male/Female/Other): ")
    contact_number = input("Enter contact number: ")
    address = input("Enter address: ")
    
    cursor = connection.cursor()
    query = """
    INSERT INTO patients (name, age, gender, contact_number, address)
    VALUES (?, ?, ?, ?, ?)
    """
    try:
        cursor.execute(query, (name, age, gender, contact_number, address))
        connection.commit()
        print(f"✅ Patient '{name}' added successfully with ID {cursor.lastrowid}")
    except sqlite3.IntegrityError:
        print("⚠️ Error: Contact number already exists! Please enter a unique number.")

# Function to generate and add a bill for a patient
def generate_bill(connection):
    patient_id = int(input("Enter patient ID: "))
    bill_amount = float(input("Enter bill amount: "))
    payment_status = input("Enter payment status (Pending/Paid): ")
    
    cursor = connection.cursor()
    query = """
    INSERT INTO bills (patient_id, bill_amount, payment_status)
    VALUES (?, ?, ?)
    """
    cursor.execute(query, (patient_id, bill_amount, payment_status))
    connection.commit()
    print(f"✅ Bill of ₹{bill_amount} added for Patient ID {patient_id}")

# Function to display patient details and their bills
def show_patient_details(connection):
    patient_id = int(input("Enter patient ID: "))
    cursor = connection.cursor()
    
    # Get patient details
    cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
    patient = cursor.fetchone()
    
    if patient:
        print(f"\n📌 Patient Details:\nID: {patient[0]}\nName: {patient[1]}\nAge: {patient[2]}\nGender: {patient[3]}\nContact: {patient[4]}\nAddress: {patient[5]}")
    else:
        print("⚠️ No patient found with this ID.")
        return
    
    # Get bill details for the patient
    cursor.execute("SELECT * FROM bills WHERE patient_id = ?", (patient_id,))
    bills = cursor.fetchall()
    
    if bills:
        print("\n💳 Bills:")
        for bill in bills:
            print(f"🔹 Bill ID: {bill[0]} | Amount: ₹{bill[2]} | Status: {bill[3]}")
    else:
        print("ℹ️ No bills found for this patient.")

# Main function to run the interactive menu
def main():
    connection = create_connection()
    if connection:
        create_tables(connection)

        while True:
            print("\n🏥 Hospital Management System")
            print("1️⃣ Add New Patient")
            print("2️⃣ Generate Bill")
            print("3️⃣ Show Patient Details")
            print("4️⃣ Exit")
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == '1':
                add_patient(connection)
            
            elif choice == '2':
                generate_bill(connection)
            
            elif choice == '3':
                show_patient_details(connection)
            
            elif choice == '4':
                print("🚪 Exiting program...")
                break
            
            else:
                print("⚠️ Invalid choice. Please enter again.")

        connection.close()

if __name__ == "__main__":
    main()
