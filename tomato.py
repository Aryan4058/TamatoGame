import ssl
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import json
import urllib.request
import base64
import io

class Smiley_Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Tomato_game")
        self.root.geometry("800x600+350+100")
        self.root.resizable(False, False)

        # Ask the user for their name
        self.name = simpledialog.askstring("Name", "Enter your name:", parent=self.root)
        if not self.name:  # If the user cancels or enters an empty name, exit the game
            self.root.destroy()
            return

        self.score = 0
        self.photo = None  # PhotoImage object

        # label for name
        self.name_label = tk.Label(root, text=f'Name: {self.name}',
                                   font=("Impact", 18, "bold"), bg='blue', fg="white")
        self.name_label.place(x=220, y=10)

        # label for score
        self.score_label = tk.Label(root, text=f'Score: {self.score}',
                                    font=("Impact", 18, "bold"), bg='white', fg="black")
        self.score_label.place(x=220, y=60)

        self.imagelab = tk.Label(root)
        self.imagelab.place(x=70, y=100)

        # Entry Input
        self.answer = tk.Entry(root, font=(
            "times new Roman", 14), bg="lightgray")
        self.answer.place(x=300, y=470, width=200, height=50)

        result = tk.Button(root, text="Submit", cursor="hand2", command=self.result_function,
                          font=("times new Roman", 14), bg="white", fg="black", activebackground="white")
        result.place(x=520, y=470, width=120)

        logout = tk.Button(root, text="Logout", cursor="hand2", command=self.logout,
                           font=("times new Roman", 14), bg="white", fg="black", activebackground="white")
        logout.place(x=650, y=470, width=120)

        self.show_image()

    @staticmethod
    def create_image():
        ssl._create_default_https_context = ssl._create_unverified_context
        api_url = "http://marcconrad.com/uob/tomato/api.php"
        response = urllib.request.urlopen(api_url)
        smile_json = json.loads(response.read())
        question = smile_json['question']
        solution = smile_json['solution']
        return question, solution

    def show_image(self):
        self.ques, self.soln = Smiley_Game.create_image()
        with urllib.request.urlopen(self.ques) as u:
            raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        self.photo = ImageTk.PhotoImage(image)

        self.imagelab.config(image=self.photo)
        self.imagelab.image = self.photo  # Keep a reference
        self.imagelab.update()

    def result_function(self):
        if self.answer.get() == "":
            messagebox.showerror("Error", "Please submit the answer", parent=self.root)
        elif self.answer.get() != str(self.soln):
            messagebox.showerror("Error", "Try Again!", parent=self.root)
            self.answer.delete(0, tk.END)
        else:
            messagebox.showinfo("Success", "Correct Answer!", parent=self.root)
            self.score += 1
            self.answer.delete(0, tk.END)
            self.score_label.config(text=f'Score: {self.score}')
            self.show_image()

    def logout(self):
        self.root.destroy()
        main()

def main():
    root = tk.Tk()                                       # Creating the root window
    img = Smiley_Game(root)                              # Initializing the Smiley_Game object
    root.config(bg='blue')                               # Setting the background color of the root window
    root.mainloop()                                      # Starting the main event loop

if __name__ == '_main_':
    main()