# Student Management System — Enterprise Hub

An enterprise-grade desktop management application built in Python using **Tkinter** and **SQLite3**. Features a modern dark-mode interface, real-time KPI metrics, instant search filtering, and complete CRUD (Create, Read, Update, Delete) capability with relational integrity.

---

## Key Features

- **Modern Dashboard UI:** Built with custom `ttk.Style` themes, dark slate backgrounds, rounded visual hierarchy, and interactive hover-responsive controls.
- **Live KPI Analytics:** Instant dynamic computation of total enrolled students, cohort GPA average, and at-risk students ($< 75\%$ attendance).
- **Persistent Storage:** Serverless, reliable storage powered by SQLite3 with primary key deduplication and validation guards.
- **Real-Time Search & Filter:** Instant multi-field querying across Roll Numbers, Student Names, and Enrolled Courses with dynamic row re-rendering.
- **Alternating Data Grid:** High-legibility `Treeview` layout featuring zebra striping, custom column alignment, and click-to-populate form binding.

---

## Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Python 3.8+** | Core programming language |
| **Tkinter / ttk** | Desktop graphical user interface framework |
| **SQLite3** | Embedded relational database management system |

---

## Project Structure

```text
student-management-system/
├── app.py                # Main application script (GUI & SQLite logic)
├── student_records.db    # SQLite database (auto-generated on first run)
├── README.md             # Project documentation
└── .gitignore            # Git ignore file
```

---

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS students (
    roll_no     TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    course      TEXT NOT NULL,
    gpa         REAL NOT NULL,
    attendance  REAL NOT NULL
);
```

---

## Getting Started

### Prerequisites

Python 3.8 or higher is required. Tkinter and SQLite3 come bundled with standard Python distributions on Windows and macOS.

> **Linux Users:** If Tkinter is not pre-installed, install it via:
> ```bash
> sudo apt-get install python3-tk
> ```

### Installation & Run

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/student-management-system.git
   cd student-management-system
   ```

2. **Run the Application:**
   ```bash
   python app.py
   ```

---

## Usage Guide

1. **Enroll a Student:** Fill in Roll Number, Full Name, Course, GPA ($0.0 - 10.0$), and Attendance ($0 - 100\%$), then click **Add Student**.
2. **Edit a Record:** Select any student from the data grid. The fields will populate into the form automatically. Adjust the values and click **Update**.
3. **Delete a Record:** Click on a row in the table, select **Delete**, and confirm the prompt.
4. **Search:** Start typing in the search bar. The table filters automatically across Roll Number, Name, and Course. Click **Refresh** to restore the full view.

---

## Roadmap

- [ ] Export records to Excel / CSV format using `pandas`
- [ ] Visual analytics dashboard tab (grade histograms & attendance trends via `matplotlib`)
- [ ] Student profile photo attachment support
- [ ] PDF grade sheet report generation

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
