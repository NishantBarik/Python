import mysql.connector
from mysql.connector import Error

# Function to create a database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Your MySQL host
            database='hospital_management',  # Database name
            user='root',  # MySQL username
            password='yourpassword'  # MySQL password
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to create required tables in the database
def create_tables(connection):
    cursor = connection.cursor()
    
    # Create Patients Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        patient_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        age INT,
        gender VARCHAR(10),
        contact_number VARCHAR(15),
        address TEXT
    )
    """)
    
    # Create Bills Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bills (
        bill_id INT AUTO_INCREMENT PRIMARY KEY,
        patient_id INT,
        bill_amount DECIMAL(10, 2),
        payment_status VARCHAR(20),
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
    )
    """)
    connection.commit()
    print("Tables created successfully")

# Function to add a new patient record
def add_patient(connection, name, age, gender, contact_number, address):
    cursor = connection.cursor()
    query = """
    INSERT INTO patients (name, age, gender, contact_number, address)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, age, gender, contact_number, address))
    connection.commit()
    print(f"Patient {name} added successfully")

# Function to generate and add a bill for a patient
def generate_bill(connection, patient_id, bill_amount, payment_status):
    cursor = connection.cursor()
    query = """
    INSERT INTO bills (patient_id, bill_amount, payment_status)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (patient_id, bill_amount, payment_status))
    connection.commit()
    print(f"Bill generated for patient ID {patient_id}")

# Function to display patient details and their bills
def show_patient_details(connection, patient_id):
    cursor = connection.cursor()
    
    # Get patient details
    cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
    patient = cursor.fetchone()
    
    # Get bill details for the patient
    cursor.execute("SELECT * FROM bills WHERE patient_id = %s", (patient_id,))
    bills = cursor.fetchall()
    
    if patient:
        print(f"Patient Details: \nID: {patient[0]}\nName: {patient[1]}\nAge: {patient[2]}\nGender: {patient[3]}\nContact: {patient[4]}\nAddress: {patient[5]}")
    else:
        print("No patient found with this ID.")
    
    if bills:
        print("\nBills:")
        for bill in bills:
            print(f"Bill ID: {bill[0]} | Amount: {bill[2]} | Status: {bill[3]}")
    else:
        print("No bills found for this patient.")

# Main function to run the system
def main():
    connection = create_connection()
    if connection:
        create_tables(connection)
        
        # Example of adding a new patient
        add_patient(connection, 'John Doe', 30, 'Male', '9876543210', '123, Some Street, City')
        
        # Example of generating a bill for the patient with patient_id = 1
        generate_bill(connection, 1, 1500.75, 'Pending')
        
        # Display details for patient with patient_id = 1
        show_patient_details(connection, 1)
        
        connection.close()

if __name__ == "__main__":
    main()
