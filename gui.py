import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw



class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Booking.com Tool")
        self.root.geometry("800x400")

        # Variables to store user inputs
        self.user_input1 = None
        self.user_input2 = None

        # Load background image
        self.background_image = Image.open("image/work.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Set background image
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        # Input 1
        self.label1 = tk.Label(self.root, text="HOTEL URL:", font=('Helvetica', 14), bg="lightgray")
        self.label1.place(relx=0.3, rely=0.4, anchor='e')
        self.entry1 = tk.Entry(self.root, font=('Helvetica', 14))
        self.entry1.place(relx=0.5, rely=0.4, anchor='center')

        # Input 2
        self.label2 = tk.Label(self.root, text="CSV NAME:", font=('Helvetica', 14), bg="lightgray")
        self.label2.place(relx=0.3, rely=0.5, anchor='e')
        self.entry2 = tk.Entry(self.root, font=('Helvetica', 14))
        self.entry2.place(relx=0.5, rely=0.5, anchor='center')

        # Create custom button
        button_width = 100
        button_height = 40
        button_radius = 20
        button_color = "lightblue"
        button_image = self.create_rounded_rectangle(button_width, button_height, button_radius, button_color)

        canvas = tk.Canvas(self.root, width=button_width, height=button_height, highlightthickness=0)
        canvas.place(relx=0.5, rely=0.6, anchor='center')
        canvas.create_image(0, 0, image=button_image, anchor='nw')
        canvas.create_text(button_width // 2, button_height // 2, text="Run", font=('Helvetica', 14), fill="black")
        canvas.bind("<Button-1>", self.on_run_button_click)

    def on_run_button_click(self, event):
        self.user_input1 = self.entry1.get()
        self.user_input2 = self.entry2.get()
        # Print inputs to the terminal
        # Show inputs in a message box
        messagebox.showinfo("Input Received", f"You entered:\nInput 1: {self.user_input1}\nInput 2: {self.user_input2}")
        # Close the application
        self.root.destroy()

    def create_rounded_rectangle(self, width, height, radius, color):
        rectangle = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(rectangle)
        draw.rounded_rectangle([(0, 0), (width, height)], radius=radius, fill=color)
        return ImageTk.PhotoImage(rectangle)

    def get_user_inputs(self):
        return self.user_input1, self.user_input2

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
