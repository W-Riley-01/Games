import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk

class Car:
    def __init__(self, speed=0):
        self.speed = speed  # Speed in mph
        self.odometer = 0   # Distance in miles
        self.time = 0       # Time in hours

    def accelerate(self):
        self.speed += 5  # Increase speed

    def brake(self):
        self.speed = max(0, self.speed - 5)  # Reduce speed

    def step(self):
        self.odometer += self.speed / 10  # Simulate distance
        self.time += 0.1  # Increment time

    def average_speed(self):
        if self.time > 0:
            return round(self.odometer / self.time, 2)
        return 0


class CarGameGUI:
    def __init__(self, root):
        self.car = Car()
        self.running = False

        # Main window
        root.title("Car Game")
        root.geometry("800x600")
        root.configure(bg="#87CEEB")

        # Display
        self.state_label = tk.Label(root, text=self.get_state_text(), font=("Arial", 12), bg="#87CEEB")
        self.state_label.pack(pady=5)

        # Odometer
        self.odometer_label = tk.Label(root, text="Odometer: 0 miles", font=("Arial", 12), bg="#87CEEB")
        self.odometer_label.pack(pady=5)

        # Avg Speed
        self.average_speed_label = tk.Label(root, text="Average Speed: 0 mph", font=("Arial", 12), bg="#87CEEB")
        self.average_speed_label.pack(pady=5)

        # Canvas
        self.canvas = Canvas(root, width=580, height=300, bg="#87CEEB")
        self.canvas.pack(pady=10)

        # Clouds
        self.create_cloud(50, 50)
        self.create_cloud(200, 30)
        self.create_cloud(400, 60)

        # Road
        self.road = self.canvas.create_rectangle(0, 250, 600, 300, fill="black", outline="")

        # Car image
        self.car_image = Image.open("car.png")  # Use your car image file
        self.car_image = self.car_image.resize((100, 50))  # Resize image
        self.car_photo = ImageTk.PhotoImage(self.car_image)

        # Place car
        self.car_item = self.canvas.create_image(50, 200, anchor="nw", image=self.car_photo)

        # Buttons
        button_frame = tk.Frame(root, bg="#87CEEB")
        button_frame.pack(pady=20)

        self.accelerate_button = tk.Button(button_frame, text="Accelerate", command=self.accelerate, width=12, bg="#4CAF50", fg="white")
        self.accelerate_button.grid(row=0, column=0, padx=5)

        self.brake_button = tk.Button(button_frame, text="Brake", command=self.brake, width=12, bg="#f44336", fg="white")
        self.brake_button.grid(row=0, column=1, padx=5)

        self.show_odometer_button = tk.Button(button_frame, text="Show Odometer", command=self.show_odometer, width=12, bg="#2196F3", fg="white")
        self.show_odometer_button.grid(row=1, column=0, pady=5)

        self.show_average_speed_button = tk.Button(button_frame, text="Show Avg Speed", command=self.show_average_speed, width=12, bg="#FFC107", fg="black")
        self.show_average_speed_button.grid(row=1, column=1, pady=5)

        # Game loop
        self.update_game()

    def get_state_text(self):
        return f"I'm going {self.car.speed} mph!"

    def update_state(self):
        self.car.step()
        self.state_label.config(text=self.get_state_text())

    def accelerate(self):
        self.car.accelerate()
        self.running = True
        self.update_state()

    def brake(self):
        self.car.brake()
        if self.car.speed == 0:
            self.running = False
        self.update_state()

    def show_odometer(self):
        self.odometer_label.config(text=f"Odometer: {round(self.car.odometer, 2)} miles")

    def show_average_speed(self):
        avg_speed = self.car.average_speed()
        self.average_speed_label.config(text=f"Average Speed: {avg_speed} mph")

    def move_car(self):
        """Move the car horizontally based on its speed."""
        distance = self.car.speed / 5
        self.canvas.move(self.car_item, distance, 0)

        # Reset position
        car_coords = self.canvas.coords(self.car_item)
        if car_coords[0] > 580:
            self.canvas.move(self.car_item, -530, 0)

    def update_game(self):
        """Continuously update the game state."""
        if self.running:
            self.update_state()
            self.move_car()
        self.canvas.after(100, self.update_game)  # Repeat every 100ms

    def create_cloud(self, x, y):
        """Draw a cloud on the canvas at (x, y) using ovals."""
        self.canvas.create_oval(x, y, x + 50, y + 30, fill="white", outline="")
        self.canvas.create_oval(x + 20, y - 10, x + 70, y + 20, fill="white", outline="")
        self.canvas.create_oval(x + 40, y, x + 90, y + 30, fill="white", outline="")


if __name__ == "__main__":
    root = tk.Tk()
    game = CarGameGUI(root)
    root.mainloop()
