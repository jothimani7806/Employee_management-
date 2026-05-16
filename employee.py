from Dbconnection import get_connection

# ─────────────────────────────────────────────
#  INSERT
# ─────────────────────────────────────────────
def insert_employee(name, designation, department, salary, phone):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO Employee (Empname, Empdesignation, Empdepartment, Salary, Phone)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, designation, department, salary, phone))
    conn.commit()
    empno = cursor.lastrowid
    cursor.close()
    conn.close()
    return empno

# ─────────────────────────────────────────────
#  FETCH ALL
# ─────────────────────────────────────────────
def fetch_all_employees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employee ORDER BY Empno")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# ─────────────────────────────────────────────
#  FETCH BY ID
# ─────────────────────────────────────────────
def fetch_employee_by_id(empno):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employee WHERE Empno = %s", (empno,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

# ─────────────────────────────────────────────
#  SEARCH
# ─────────────────────────────────────────────
def search_employees(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    like = f"%{keyword}%"
    query = """
        SELECT * FROM Employee
        WHERE Empname LIKE %s
           OR Empdesignation LIKE %s
           OR Empdepartment LIKE %s
        ORDER BY Empno
    """
    cursor.execute(query, (like, like, like))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# ─────────────────────────────────────────────
#  UPDATE
# ─────────────────────────────────────────────
def update_employee(empno, name, designation, department, salary, phone):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        UPDATE Employee
        SET Empname = %s,
            Empdesignation = %s,
            Empdepartment = %s,
            Salary = %s,
            Phone = %s
        WHERE Empno = %s
    """
    cursor.execute(query, (name, designation, department, salary, phone, empno))
    affected = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    return affected > 0

# ─────────────────────────────────────────────
#  DELETE
# ─────────────────────────────────────────────
def delete_employee(empno):
    """Delete an employee record by Empno. Returns True if deleted."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Employee WHERE Empno = %s", (empno,))
    affected = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    return affected > 0