## README: Gym Attendance System

---

### Project Description 🏋️‍♂️
This project is a **Gym Attendance Management System** built using Python, SQLite, and Tkinter (with TTK Bootstrap for enhanced UI). It provides an efficient way to manage gym members and track daily attendance, ensuring a smooth operational flow for gym owners and administrators.

---

### Key Features 🚀

1. **Member Management:**
   - Add new members with details: Roll Number, Name, Phone Number, Date of Birth, Start Date, and End Date.
   - View all registered members in a user-friendly table format.
   - Alerts if a member with the same Roll Number already exists.

2. **Attendance Tracking:**
   - Easily mark attendance by entering a member's Roll Number.
   - Prevents duplicate attendance entries for the same day.
   - Provides sound and visual notifications if a member's subscription has expired.

3. **Subscription Monitoring:**
   - View all members whose subscriptions have expired or are expiring within the next 3 days.
   - Visual alerts with sound warnings when marking attendance for expired members.

4. **Daily Attendance Report:**
   - View all members marked as present for the current day.
   - User-friendly table layout with vertical scrolling for easy navigation.

5. **Enhanced UI/UX:**
   - Utilizes TTK Bootstrap for a modern, responsive interface.
   - Sound feedback for successful actions or errors.

---

### Technology Stack 🛠️

- **Programming Language:** Python
- **GUI Library:** Tkinter with TTK Bootstrap
- **Database:** SQLite
- **Additional Modules:** `datetime`, `winsound`

---

### Installation Instructions 💻

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/YourUsername/Gym-Attendance-System.git
   cd Gym-Attendance-System
   ```

2. **Set up a Virtual Environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install ttkbootstrap
   ```

4. **Run the Application:**
   ```bash
   python gym_attendance.py
   ```

---

### Usage Guide 📋

1. **Mark Attendance:**
   - Open the app and enter the member's Roll Number in the "Mark Attendance" section.
   - Press Enter or click the "Mark Attendance" button.

2. **Add New Members:**
   - Fill in all required fields in the "Add New Member" section.
   - Click the "Add Member" button to save the member details.

3. **View Reports:**
   - Click on "View Members" to see the member list.
   - Use "View Today's Attendance" for the current day's attendance record.
   - Click "View Expiring Subscriptions" to track subscriptions nearing expiration.

---

### Screenshots 📸
Add screenshots here showcasing different parts of the application, such as:
1. Main dashboard.   ![image](https://github.com/user-attachments/assets/53c6b96c-bf09-4df2-8f12-4eb5da5b0d35)
2. Mark Attendance form. ![image](https://github.com/user-attachments/assets/127d2b83-ad17-4453-b534-38603b6b9437)
3. Add Member form.  ![image](https://github.com/user-attachments/assets/fe8acedc-d857-46ba-8148-c2f6d8e2b618)
4. Member and Attendance reports. ![image](https://github.com/user-attachments/assets/19bb7abb-c0b0-4a95-a0d1-1b331dbc810a)


---

### Contribution 🤝
Contributions are welcome! Feel free to:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`
3. Commit your changes: `git commit -m 'Add new feature'`
4. Push the branch: `git push origin feature-branch`
5. Submit a pull request.

---

### License 📄
This project is licensed under the [MIT License](LICENSE).

---

### Connect with Me 👋
**Aishwary Gupta**
- LinkedIn: (www.linkedin.com/in/aishwary-gupta-b734a2327)
- GitHub: [Aishwary-gupta](https://github.com/Aishwary-gupta)

---

