#HRI

import tkinter as tk

class HRI:

    def __init__(self):

        self.root = tk.Tk()
        self.root.geometry("700x500")
        self.root.configure(bg="#33ccff")
        self.root.title("LLM Robot")

        self.frame = tk.Frame(self.root, bg="#3366ff")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        self.label_1 = tk.Label(self.frame, text="What would you like 'Henry The Robot' to do?", font=('Arial', 20), bg="#3366ff")
        self.label_1.place(relx=0.5, rely=0.2, anchor="center")

        self.label_2 = tk.Label(self.frame, text="Please speak as naturally as possible!", font=('Arial', 12), bg="#3366ff")
        self.label_2.place(relx=0.5, rely=0.3, anchor="center")

        self.textbox = tk.Text(self.frame, height=3,font=('Arial', 12))
        self.textbox.place(relx=0.5, rely=0.6, anchor="center")
        self.textbox.config(width=60)

        self.perform_btn = tk.Button(self.frame, text="Perform Task",font=('Arial', 15), bg="#4b25bd")
        self.perform_btn.place(relx=0.5, rely=0.9, anchor="center")

        self.root.mainloop()


hri = HRI()

