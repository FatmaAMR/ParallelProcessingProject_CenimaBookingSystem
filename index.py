import tkinter as tk
from tkinter import messagebox
import threading
import sqlite3

# Database Setup
def setup_database():
    conn = sqlite3.connect('movie_booking_system.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS halls (
                        hall_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        hall_name TEXT UNIQUE NOT NULL,
                        total_seats INTEGER NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS movies (
                        movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        movie_name TEXT NOT NULL,
                        hall_id INTEGER NOT NULL,
                        start_hour TEXT NOT NULL,
                        end_hour TEXT NOT NULL,
                        FOREIGN KEY(hall_id) REFERENCES halls(hall_id)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS tickets (
                        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_name TEXT NOT NULL,
                        movie_id INTEGER NOT NULL,
                        seat_number INTEGER NOT NULL,
                        FOREIGN KEY(movie_id) REFERENCES movies(movie_id)
                    )''')

    conn.commit()
    conn.close()

class Movie:
    def __init__(self, movie_id, name, hall_id, start_hour, end_hour):
        self.movie_id = movie_id
        self.name = name
        self.hall_id = hall_id
        self.start_hour = start_hour
        self.end_hour = end_hour
        
class Ticket:
    def __init__(self, ticket_id, user_name, movie_id, seat_number):
        self.ticket_id = ticket_id
        self.user_name = user_name
        self.movie_id = movie_id
        self.seat_number = seat_number
        
class Admin:
    @staticmethod
    def add_movie(movie_name, hall_id, start_hour, end_hour):
        try:
            conn = sqlite3.connect('movie_booking_system.db')
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO movies (movie_name, hall_id, start_hour, end_hour) VALUES (?, ?, ?, ?)',
                (movie_name, hall_id, start_hour, end_hour)
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def remove_movie(movie_id):
        try:
            conn = sqlite3.connect('movie_booking_system.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM movies WHERE movie_id = ?', (movie_id,))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def edit_movie(movie_id, new_name, hall_id, start_hour):
        try:
            conn = sqlite3.connect('movie_booking_system.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE movies SET movie_name = ? , hall_id = ?, start_hour= ? WHERE movie_id = ?', (new_name,  hall_id, start_hour,  movie_id))
            
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def fetch_movies():
        try:
            conn = sqlite3.connect('movie_booking_system.db')
            cursor = conn.cursor()
            cursor.execute('SELECT movie_id, movie_name FROM movies')
            return cursor.fetchall()
        finally:
            conn.close()

# Login Screen
def admin_login(master):
    def verify_credentials():
        username = username_entry.get()
        password = password_entry.get()

        if username == "Fatma" and password == "0000":
            admin_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    login_window = tk.Toplevel(master)
    login_window.title("Admin Login")
    login_window.geometry("300x200")

    tk.Label(login_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    tk.Button(login_window, text="Login", command=verify_credentials).pack(pady=10)

# Admin Dashboard
def admin_dashboard():
    dashboard = tk.Toplevel()
    dashboard.title("Admin Dashboard")
    dashboard.geometry("800x800")

    def refresh_movies():
        for widget in movies_frame.winfo_children():
            widget.destroy()

        movies = Admin.fetch_movies()
        for movie_id, movie_name in movies:
            tk.Label(movies_frame, text=f"{movie_id}. {movie_name}").pack()

    def add_movie():
        try:
            Admin.add_movie(movie_name_entry.get(), int(hall_id_entry.get()), start_hour_entry.get(), end_hour_entry.get())
            messagebox.showinfo("Success", "Movie added successfully.")
            refresh_movies()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def remove_movie():
        try:
            Admin.remove_movie(int(remove_movie_id_entry.get()))
            messagebox.showinfo("Success", "Movie removed successfully.")
            refresh_movies()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def edit_movie():
        try:
            Admin.edit_movie(int(edit_movie_id_entry.get()),edit_movie_name_entry.get(), int(edit_hall_id_entry.get()), edit_start_hour_entry.get())
            messagebox.showinfo("Success", "Movie updated successfully.")
            refresh_movies()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Label(dashboard, text="Movies Dashboard", font=("Arial", 16, "bold")).pack(pady=10)

    tk.Label(dashboard, text="Movie ID:").pack()
    movie_id_entry = tk.Entry(dashboard)
    movie_id_entry.pack()

    tk.Label(dashboard, text="Movie Name:").pack()
    movie_name_entry = tk.Entry(dashboard)
    movie_name_entry.pack()

    tk.Label(dashboard, text="Hall ID:").pack()
    hall_id_entry = tk.Entry(dashboard)
    hall_id_entry.pack()

    tk.Label(dashboard, text="Start Hour:").pack()
    start_hour_entry = tk.Entry(dashboard)
    start_hour_entry.pack()

    tk.Label(dashboard, text="End Hour:").pack()
    end_hour_entry = tk.Entry(dashboard)
    end_hour_entry.pack()

    tk.Button(dashboard, text="Add Movie", command=add_movie).pack(pady=5)
    #-----------------------------------
    
    tk.Label(dashboard, text="Id of movie to remove").pack()
    remove_movie_id_entry = tk.Entry(dashboard)
    remove_movie_id_entry.pack()
    tk.Button(dashboard, text="Remove Movie", command=remove_movie).pack(pady=5)
    #----------editMovie-------
    tk.Label(dashboard, text="Movie ID to edit:").pack()
    edit_movie_id_entry = tk.Entry(dashboard)
    edit_movie_id_entry.pack()

    tk.Label(dashboard, text=" New Movie Name:").pack()
    edit_movie_name_entry = tk.Entry(dashboard)
    edit_movie_name_entry.pack()

    tk.Label(dashboard, text="New Hall ID:").pack()
    edit_hall_id_entry = tk.Entry(dashboard)
    edit_hall_id_entry.pack()

    tk.Label(dashboard, text="New Start Hour:").pack()
    edit_start_hour_entry = tk.Entry(dashboard)
    edit_start_hour_entry.pack()

    tk.Button(dashboard, text="Edit Movie", command=edit_movie).pack(pady=5)

    movies_frame = tk.Frame(dashboard)
    movies_frame.pack(pady=20)

    refresh_movies()

# Main Start Window
def start_window():
    root = tk.Tk()
    root.title("Cinema System")
    root.geometry("400x200")

    tk.Label(root, text="Welcome to Cinema System", font=("Arial", 14, "bold")).pack(pady=20)

    tk.Button(root, text="Ticket Window Simulation", command=lambda: start_booking_system(root)).pack(pady=10)
    tk.Button(root, text="Login as Admin", command=lambda: admin_login(root)).pack(pady=10)

    root.mainloop()

class MovieBookingSystem:
    def __init__(self, master, num_users, mode):
        self.master = master
        self.num_users = num_users
        self.mode = mode
        self.lock = threading.Lock()

        # Start the system based on the mode
        if self.mode == 'Multithreading':
            self.create_user_threads()
        else:
            self.create_user_sequential()

    def create_user_threads(self):
        for user_num in range(self.num_users):
            threading.Thread(target=self.show_movies, args=(user_num + 1,)).start()

    def create_user_sequential(self):
        for user_num in range(self.num_users):
            movie_window = self.show_movies(user_num + 1)
            self.master.wait_window(movie_window)

    def fetch_movies(self):
        conn = sqlite3.connect('movie_booking_system.db')
        cursor = conn.cursor()
        cursor.execute('SELECT movie_id, movie_name, hall_id, start_hour, end_hour FROM movies')
        movies = [Movie(*row) for row in cursor.fetchall()]
        conn.close()
        return movies

    def fetch_halls(self):
        conn = sqlite3.connect('movie_booking_system.db')
        cursor = conn.cursor()
        cursor.execute('SELECT hall_id, hall_name, total_seats FROM halls')
        halls = cursor.fetchall()
        conn.close()
        return halls

    def show_movies(self, user_num):
        movie_window = tk.Toplevel(self.master)
        movie_window.title(f"User {user_num} - Select a Movie")
        movie_window.geometry("400x300")

        movies = self.fetch_movies()

        if not movies:
            tk.Label(movie_window, text="No movies available.", fg="red").pack(pady=20)
        else:
            tk.Label(movie_window, text="Available Movies:", font=("Arial", 14, "bold")).pack(pady=10)
            for movie in movies:
                tk.Button(movie_window, text=f"{movie.name} ({movie.start_hour} - {movie.end_hour})",
                          command=lambda m=movie: self.show_halls(user_num, m)).pack(pady=5)

        return movie_window

    def show_halls(self, user_num, movie):
        hall_window = tk.Toplevel(self.master)
        hall_window.title(f"User {user_num} - Select a Seat in {movie.name}")
        hall_window.geometry("600x400")

        conn = sqlite3.connect('movie_booking_system.db')
        cursor = conn.cursor()

        cursor.execute('SELECT total_seats FROM halls WHERE hall_id = ?', (movie.hall_id,))
        total_seats = cursor.fetchone()[0]

        cursor.execute('SELECT seat_number FROM tickets WHERE movie_id = ?', (movie.movie_id,))
        booked_seats = [row[0] for row in cursor.fetchall()]

        conn.close()

        for seat in range(1, total_seats + 1):
            if seat in booked_seats:
                seat_button = tk.Button(hall_window, text=f"Seat {seat} - Booked", state=tk.DISABLED, bg="red", fg="white")
            else:
                seat_button = tk.Button(hall_window, text=f"Seat {seat}",
                                        command=lambda s=seat: self.book_ticket(user_num, movie, s, hall_window))
            seat_button.grid(row=(seat - 1) // 5, column=(seat - 1) % 5, padx=5, pady=5)

    def book_ticket(self, user_num, movie, seat, hall_window):
        with self.lock:
            conn = sqlite3.connect('movie_booking_system.db')
            cursor = conn.cursor()

            cursor.execute('SELECT 1 FROM tickets WHERE movie_id = ? AND seat_number = ?', (movie.movie_id, seat))
            if cursor.fetchone():
                conn.close()
                messagebox.showerror("Booking Failed", "Seat already booked.")
                return

            cursor.execute('INSERT INTO tickets (user_name, movie_id, seat_number) VALUES (?, ?, ?)',
                           (f"User {user_num}", movie.movie_id, seat))
            conn.commit()
            conn.close()

            messagebox.showinfo("Booking Successful", f"Seat {seat} successfully booked for {movie.name}!")
            hall_window.destroy()


# Booking System Start
def start_booking_system(master):
    root = tk.Toplevel(master)
    root.title("Movie Booking System")
    root.geometry("400x200")

    def start_system():
        try:
            num_users = int(num_users_entry.get())
            if num_users <= 0:
                raise ValueError("Number of users must be greater than 0")

            def choose_mode(mode):
                mode_window.destroy()
                MovieBookingSystem(root, num_users, mode)

            mode_window = tk.Toplevel(root)
            mode_window.title("Select Mode")
            mode_window.geometry("300x150")

            tk.Button(mode_window, text="Multithreading", command=lambda: choose_mode('Multithreading')).pack(pady=10)
            tk.Button(mode_window, text="Sequential", command=lambda: choose_mode('Sequential')).pack(pady=10)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of users.")

    tk.Label(root, text="Enter the number of users:").pack(pady=10)
    num_users_entry = tk.Entry(root)
    num_users_entry.pack(pady=10)

    tk.Button(root, text="Start", command=start_system).pack(pady=10)

if __name__ == "__main__":
    setup_database()
    start_window()
