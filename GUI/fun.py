import customtkinter as tk

tk.set_appearance_mode("dark")
tk.set_default_color_theme("green")

passwords = []
with open("GUI/passwords.txt") as f:
   passwordList = f.read().splitlines()
for i in passwordList:
    passwords.append(i)

def Login():
    for i in passwords:
        if username.get() == i.split(" : ")[0] and password.get() == i.split(" : ")[1]:
            return True
    return False

def Login_Page():
    if not Login():
        loginMessage.configure(text="Incorrect username or password")
    else:
        loginMessage.configure(text="Login successful")
        root.destroy()
        Home_Page()

def Home_Page():
    root = tk.CTk()
    root.geometry("500x350")

    frame = tk.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = tk.CTkLabel(master=frame, text="Home", font=("Arial", 24))
    label.pack(pady=12, padx=10)

    choice1 = tk.CTkButton(master=frame, text="Choice 1", command=Home_Page)
    choice1.pack(pady=12, padx=10)

    choice2 = tk.CTkButton(master=frame, text="Choice 2", command=Home_Page)
    choice2.pack(pady=12, padx=10)

    root.mainloop()

root = tk.CTk()
root.geometry("500x350")

frame = tk.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = tk.CTkLabel(master=frame, text="Login", font=("Arial", 24))
label.pack(pady=12, padx=10)

username = tk.CTkEntry(master=frame, placeholder_text="Username")
username.pack(pady=12, padx=10)

password = tk.CTkEntry(master=frame, placeholder_text="Password", show="*")
password.pack(pady=12, padx=10)

button = tk.CTkButton(master=frame, text="Login", command=Login_Page)
button.pack(pady=12, padx=10)

loginMessage = tk.CTkLabel(master=frame, text="", font=("Arial", 12, "bold"))
loginMessage.pack(pady=12, padx=10)

root.mainloop()
