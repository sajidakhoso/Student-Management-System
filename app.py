import streamlit as st
import os
import csv
from typing import List, Dict

# ---------- GLOBAL CONFIG ----------
DATA_FILE = "students.txt"
FIELDNAMES = ["ID", "Name", "Age", "Grade", "Section"]

# ---------- FILE FUNCTIONS ----------
def ensure_data_file():
    """Create the data file if it does not exist."""
    if not os.path.exists(DATA_FILE):
        open(DATA_FILE, "w", encoding="utf-8").close()

def read_records() -> List[Dict[str, str]]:
    ensure_data_file()
    records = []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 5:
                records.append(dict(zip(FIELDNAMES, row)))
    return records

def write_records(records: List[Dict[str, str]]):
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for r in records:
            writer.writerow([r[field] for field in FIELDNAMES])

# ---------- VALIDATION ----------
def validate_student(id, name, age, grade, section, existing_ids):
    if not id.isdigit():
        return False, "❌ Student ID must be numeric."
    if id in existing_ids:
        return False, "⚠️ Student ID already exists."
    if not name.strip():
        return False, "❌ Name cannot be empty."
    if not age.isdigit() or int(age) <= 0:
        return False, "❌ Age must be a positive number."
    if grade.upper() not in ["A", "B", "C", "D", "E", "F"]:
        return False, "❌ Grade must be between A–F."
    if not section.strip():
        return False, "❌ Section cannot be empty."
    return True, "OK"

# ---------- CORE OPERATIONS ----------
def add_student(id, name, age, grade, section):
    records = read_records()
    ids = [r["ID"] for r in records]
    valid, msg = validate_student(id, name, age, grade, section, ids)
    if not valid:
        return False, msg
    records.append({"ID": id, "Name": name, "Age": age, "Grade": grade.upper(), "Section": section})
    write_records(records)
    return True, "✅ Student added successfully!"

def search_student(id):
    return next((r for r in read_records() if r["ID"] == id), None)

def update_student(id, name, age, grade, section):
    records = read_records()
    updated = False
    for r in records:
        if r["ID"] == id:
            r.update({"Name": name, "Age": age, "Grade": grade.upper(), "Section": section})
            updated = True
            break
    if updated:
        write_records(records)
        return True, "✅ Record updated successfully!"
    return False, "❌ Student ID not found."

def delete_student(id):
    records = read_records()
    new_records = [r for r in records if r["ID"] != id]
    if len(new_records) == len(records):
        return False, "❌ Student not found."
    write_records(new_records)
    return True, "🗑️ Student deleted."

# ---------- UI ----------
st.set_page_config(page_title="SMS by Sajida Khoso", layout="wide")

# Branding Header
st.markdown("""
<h1 style="text-align:center; color:#4CAF50;">📚 Student Management System</h1>
<h4 style="text-align:center; color:#666;">Developed with ❤️ by <b style="color:#E91E63;">Sajida Khoso</b></h4>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("📌 Actions")
choice = st.sidebar.selectbox(
    "Select",
    ["Home", "Add Student", "View All Students", "Search Student", "Update Student", "Delete Student", "About"]
)

# GitHub Button
st.sidebar.markdown("""
<a href='https://github.com/sajidakhoso' target='_blank'>
    <button style='background:#4CAF50;color:white;padding:8px 12px;border:none;border-radius:6px;width:100%;'>
    🌐 Sajida's GitHub
    </button>
</a>
""", unsafe_allow_html=True)

# ---------- PAGES ----------
if choice == "Home":
    st.header("🏠 Welcome to the Student Management System")
    st.info("Use the left sidebar to manage student records.")

elif choice == "Add Student":
    st.header("➕ Add New Student")
    id = st.text_input("Student ID")
    name = st.text_input("Full Name")
    age = st.text_input("Age")
    grade = st.text_input("Grade (A-F)")
    section = st.text_input("Section")
    if st.button("Add Student"):
        ok, msg = add_student(id, name, age, grade, section)
        if ok:
            st.success(msg)
        else:
            st.error(msg)

elif choice == "View All Students":
    st.header("📋 All Students")
    data = read_records()
    if data:
        st.table(data)
    else:
        st.warning("No students found.")

elif choice == "Search Student":
    st.header("🔍 Search Student")
    id = st.text_input("Enter Student ID")
    if st.button("Search"):
        rec = search_student(id)
        if rec:
            st.success("Student Found:")
            st.json(rec)
        else:
            st.error("Not found.")

elif choice == "Update Student":
    st.header("✏️ Update Student")
    id = st.text_input("Enter ID to update")
    if st.button("Load Record"):
        rec = search_student(id)
        if rec:
            st.session_state["edit"] = rec
        else:
            st.error("No record found.")
    if "edit" in st.session_state:
        rec = st.session_state["edit"]
        name = st.text_input("Name", rec["Name"])
        age = st.text_input("Age", rec["Age"])
        grade = st.text_input("Grade (A-F)", rec["Grade"])
        section = st.text_input("Section", rec["Section"])
        if st.button("Save Changes"):
            ok, msg = update_student(rec["ID"], name, age, grade, section)
            if ok:
                st.success(msg)
            else:
                st.error(msg)
            st.session_state.pop("edit", None)

elif choice == "Delete Student":
    st.header("🗑️ Delete Student")
    id = st.text_input("Enter Student ID")
    if st.button("Delete"):
        ok, msg = delete_student(id)
        if ok:
            st.success(msg)
        else:
            st.error(msg)

elif choice == "About":
    st.header("ℹ️ About This Project")
    st.write("""
    **Student Management System**  
    Created by **Sajida Khoso**  
    ✔ Built with Python  
    ✔ Backend: CSV File  
    ✔ CRUD Operations  
    ✔ User-friendly Interface  
    """)
    st.success("Thank you for using the Student Management System!")

# ---------- FOOTER ----------
st.markdown("""
<br>
<hr>
<center>
🌸 Developed with ❤️ by <b style="color:#E91E63;">Sajida Khoso</b>  
<br>
<a href='https://github.com/sajidakhoso' target='_blank'>🔗 GitHub Profile</a>
</center>
""", unsafe_allow_html=True)
