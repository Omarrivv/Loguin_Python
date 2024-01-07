from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3
import hashlib
class WelcomeWindow:
    def __init__(self, username):
        self.root = Toplevel()
        self.root.title("Bienvenido")
        self.root.geometry("300x200+500+200")
        Label(self.root, text=f"Bienvenido, {username}!", font=("Arial Black", 14)).pack()
        Button(self.root, text="Cerrar", command=self.root.destroy, bg='#a6d4f2', font=("Arial Rounded MT Bold", 10)).pack()
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login CodeFxRoma")
        self.root.geometry("500x400+300+250")
        self.color = '#c5e2f6'
        self.root['bg'] = self.color
        Label(root, bg=self.color, text="Login CodeFxRoma", font=("Arial Black", 20)).pack()

        # Abrir imagen para ventana principal
        self.load_and_display_image("logoia.jpeg", (180, 180))

        Label(root, text="Usuario:", bg=self.color, font=("Arial Black", 10)).pack()
        self.username_entry = Entry(root, font=("Arial", 10))
        self.username_entry.pack()

        Label(root, text="Contraseña:", bg=self.color, font=("Arial Black", 10)).pack()
        self.password_entry = Entry(root, show="*")
        self.password_entry.pack()

        Button(root, text="Entrar", command=self.login, bg='#a6d4f2', font=("Arial Rounded MT Bold", 10)).pack()
        Label(root, text="No tienes una cuenta?", bg=self.color, font=("Arial Black", 10)).pack()
        Button(root, text="Registro", command=self.open_registration_window, bg='#a6d4f2', font=("Arial Rounded MT Bold", 10)).pack()

    def load_and_display_image(self, image_path, size):
        image = Image.open(image_path)
        image = image.resize(size, Image.LANCZOS)
        photo_img = ImageTk.PhotoImage(image)
        panel = Label(self.root, image=photo_img)
        panel.image = photo_img  # Keep a reference to avoid garbage collection
        panel.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Hash the password before comparing
        hashed_password = self.hash_password(password)

        # Connect to the database
        with sqlite3.connect('login.db') as db:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE Usuario = ? AND Pass = ?', (username, hashed_password))

            if cursor.fetchall():
                # Crear una instancia de la ventana de bienvenida si el inicio de sesión es exitoso
                welcome_window = WelcomeWindow(username)
                messagebox.showinfo(title="Login Correcto", message="Usuario y contraseña correctos")
            else:
                messagebox.showerror(title="Login incorrecto", message="Usuario o contraseña incorrecto")

    def open_registration_window(self):
        registration_window = Toplevel(self.root)
        registration_window.title("Registro de Usuario")
        registration_window.geometry("300x290+800+250")
        registration_window['bg'] = self.color

        Label(registration_window, text="Registro:", bg=self.color, font=("Arial Black", 12)).pack(side="top")

        # Abrir imagen para ventana de registro
        self.load_and_display_image("logoia.jpeg", (100, 220))

        Label(registration_window, text="Nombre:", bg=self.color, font=("Arial Black", 10)).pack()
        self.name_entry = Entry(registration_window)
        self.name_entry.pack()

        Label(registration_window, text="Apellidos:", bg=self.color, font=("Arial Black", 10)).pack()
        self.lastname_entry = Entry(registration_window)
        self.lastname_entry.pack()

        Label(registration_window, text="Usuario:", bg=self.color, font=("Arial Black", 10)).pack()
        self.username_entry_reg = Entry(registration_window)
        self.username_entry_reg.pack()

        Label(registration_window, text="Contraseña:", bg=self.color, font=("Arial Black", 10)).pack()
        self.password_entry_reg = Entry(registration_window, show="*")
        self.password_entry_reg.pack()

        Label(registration_window, text="Repita la Contraseña:", bg=self.color, font=("Arial Black", 10)).pack()
        self.password_confirm_entry = Entry(registration_window, show="*")
        self.password_confirm_entry.pack()

        Button(registration_window, text="Registrar", command=self.register_user, bg=self.color,
               font=("Arial Rounded MT Bold", 10)).pack(side="bottom")

    def register_user(self):
        name = self.name_entry.get()
        lastname = self.lastname_entry.get()
        username = self.username_entry_reg.get()
        password = self.password_entry_reg.get()
        password_confirm = self.password_confirm_entry.get()

        # Validate inputs
        if not all([name, lastname, username, password, password_confirm]):
            messagebox.showerror(title="Campos vacíos", message="Todos los campos son obligatorios.")
            return

        if password != password_confirm:
            messagebox.showerror(title="Contraseña Incorrecta", message="Las contraseñas no coinciden.")
            return

        # Hash the password before storing
        hashed_password = self.hash_password(password)

        # Connect to the database
        with sqlite3.connect('login.db') as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO usuarios VALUES (?, ?, ?, ?)", (name, lastname, username, hashed_password))
            db.commit()
            messagebox.showinfo(title="Registro Correcto", message=f"Hola {name} {lastname}.\n¡Tu registro fue exitoso!")
    def hash_password(self, password):
        # Use a secure hash function like SHA-256
        hashed = hashlib.sha256(password.encode()).hexdigest()
        return hashed

if __name__ == "__main__":
    root = Tk()
    app = LoginApp(root)
    root.mainloop()