from customtkinter import *
import random
import threading

ROWS = 10
BALLS = 100
DELAY = 0.0001

class GaltonBoard:
    def __init__(self) -> None:
      
        self.window = CTk()
        self.total_width, self.total_height = 600, 600
        self.window.geometry(f"{self.total_width}x{self.total_height}")
        self.window.title("Доска Гальтона")
        self.window._set_appearance_mode("dark")
        self.window.resizable(width=False, height=False)

        
        self.bins = [0] * (ROWS + 1)
        self.pegs = []
        self.bin_rects = []
        self.bin_width = 580 // (ROWS + 1)

        
        self.canvas = CTkCanvas(self.window, width=580, height=520, bg="gray", highlightthickness=0)
        self.canvas.pack(padx=10, pady=(20, 10))

        
        self.start_button = CTkButton(
            self.window,
            text="Запустить",
            command=self.run_simulation,
            font=CTkFont(family='Benzin-Bold', size=20),
            text_color='black',
            fg_color='white',
            hover=False,
            bg_color='transparent'
        )
        self.start_button.pack(pady=10)

        
        self.draw_pegs()
        self.draw_bins()


    def draw_pegs(self):
        center_x = 580 // 2
        start_y = 60

        dx = 40  
        dy = 40  

        self.pegs = []

        for row in range(ROWS):
            y = start_y + row * dy
            row_pegs = []

            row_start_x = center_x - (row * dx) // 2

            for col in range(row + 1):
                x = row_start_x + col * dx
                peg = self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")
                row_pegs.append((x, y))
            self.pegs.append(row_pegs)

    def draw_bins(self):
        for i in range(ROWS + 1):
            x1 = i * self.bin_width
            y1 = 500
            x2 = x1 + self.bin_width - 2
            y2 = 520
            rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightgray")
            self.bin_rects.append(rect)

    def animate_ball(self):
        center_x = 580 // 2
        dx = 40
        dy = 40

        x = center_x
        y = 20
        ball = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red", outline="")

        position = 0
        for row in range(ROWS):
            threading.Event().wait(DELAY)
            direction = random.choice([-1, 1])
            position += 1 if direction == 1 else 0

            x += (dx // 2) * direction
            y += dy
            self.canvas.coords(ball, x - 5, y - 5, x + 5, y + 5)
            self.window.update_idletasks()

        self.canvas.delete(ball)
        self.bins[position] += 1
        self.update_bins()

    def update_bins(self):
        for i, count in enumerate(self.bins):
            height = count * 3
            x1 = i * self.bin_width
            y1 = 520 - height
            x2 = x1 + self.bin_width - 2
            self.canvas.coords(self.bin_rects[i], x1, y1, x2, 520)
            self.canvas.itemconfig(self.bin_rects[i], fill="blue")

    def run_simulation(self):
        def simulation_thread():
            self.start_button.configure(state="disabled")
            for _ in range(BALLS):
                self.animate_ball()
            self.start_button.configure(state="normal")
        threading.Thread(target=simulation_thread, daemon=True).start()

    def close(self):
        self.window.destroy()

    def run(self):
        self.window.mainloop()



if __name__ == "__main__":
    app = GaltonBoard()
    app.run()

