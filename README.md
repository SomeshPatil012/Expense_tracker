The **Personal Expense Tracker** is a simple yet powerful application designed to help users log, manage, and review their daily expenses in a structured way. Built using Python’s Tkinter library for the graphical interface and SQLite for data storage, this app is ideal for anyone seeking an easy method to track personal finances.

### Key Features:

1. **Expense Logging**: Users can add expenses by entering a description and amount in a form, which are then saved in an SQLite database. The app validates that each entry has a positive numeric amount and requires both fields to be filled out, ensuring data integrity.

2. **Real-time Totals**: The app displays a real-time total of all recorded expenses, automatically updating whenever an expense is added or deleted. This feature makes it easy for users to monitor their spending at a glance.

3. **Interactive Expense Table**: All expenses are displayed in a sortable table, showing each record’s ID, description, and amount. A dropdown menu allows users to choose the sort order—by ID, description, or amount—offering flexibility for data review and comparison.

4. **Expense Deletion**: Users can remove specific expenses by selecting them from the table and clicking “Delete.” This feature is useful for correcting mistakes or managing records over time.

5. **Search Functionality**: A search bar allows users to filter expenses based on description keywords. This makes it easy to locate specific expenses without manually scrolling through the table.

6. **User-Friendly Design**: The app’s interface is organized with frames for each functional section (input, display, search, and sorting). Thoughtful color choices, clear labels, and well-placed buttons enhance the user experience.

### Technical Details:

- **Data Persistence**: SQLite ensures that all expenses remain available across sessions, so users do not lose data when the app is closed.
- **Efficiency**: The app is lightweight, focusing on simplicity and essential features, making it accessible to users with varying tech experience.

The **Personal Expense Tracker** provides a straightforward, reliable, and organized way to manage daily expenses in a single window.

![image](https://github.com/user-attachments/assets/527e3792-6f52-445c-b263-c450544b9768)
