import tkinter as tk
import random

class DinoGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Chrome Dino Game")
        self.root.geometry("800x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#f7f7f7")
        
        self.canvas = tk.Canvas(root, width=800, height=300, bg="#f7f7f7", highlightthickness=0)
        self.canvas.pack(pady=20)
        
        # Game state
        self.running = False
        self.game_over = False
        self.score = 0
        self.high_score = 0
        self.speed = 8
        self.gravity = 1.2
        self.jump_power = -18
        
        # Dino
        self.dino_x = 80
        self.dino_y = 220
        self.dino_vel_y = 0
        self.dino_on_ground = True
        self.dino_frame = 0
        
        # Obstacles
        self.obstacles = []
        self.obstacle_timer = 0
        
        # Ground
        self.ground_x = 0
        
        # Clouds
        self.clouds = []
        self.init_clouds()
        
        # UI
        self.score_label = tk.Label(root, text="Score: 0  |  HI: 0", font=("Courier New", 16, "bold"), 
                                     fg="#535353", bg="#f7f7f7")
        self.score_label.pack()
        
        self.status_label = tk.Label(root, text="Press SPACE to start", font=("Courier New", 14), 
                                      fg="#999", bg="#f7f7f7")
        self.status_label.pack(pady=10)
        
        # Bind keys
        self.root.bind("<space>", self.on_space)
        self.root.bind("<Up>", self.on_space)
        self.root.bind("<Down>", self.on_down)
        self.root.bind("<r>", self.restart)
        self.root.focus_set()
        
        self.draw_static()
        self.game_loop()
    
    def init_clouds(self):
        for _ in range(4):
            x = random.randint(0, 800)
            y = random.randint(30, 120)
            speed = random.uniform(0.5, 1.5)
            self.clouds.append([x, y, speed])
    
    def draw_static(self):
        self.canvas.delete("all")
        
        # Ground line
        self.canvas.create_line(0, 250, 800, 250, fill="#c5c5c5", width=2)
        
        # Clouds
        for cloud in self.clouds:
            x, y, _ = cloud
            self.draw_cloud(x, y)
        
        # Dino
        self.draw_dino()
        
        # Obstacles
        for obs in self.obstacles:
            self.draw_obstacle(obs)
    
    def draw_cloud(self, x, y):
        self.canvas.create_oval(x, y, x+40, y+20, fill="#fff", outline="#e0e0e0", width=1)
        self.canvas.create_oval(x+15, y-10, x+50, y+15, fill="#fff", outline="#e0e0e0", width=1)
        self.canvas.create_oval(x+30, y, x+65, y+20, fill="#fff", outline="#e0e0e0", width=1)
    
    def draw_dino(self):
        x, y = self.dino_x, self.dino_y
        # Body
        self.canvas.create_rectangle(x, y, x+40, y+40, fill="#535353", outline="#535353")
        # Eye
        self.canvas.create_oval(x+28, y+10, x+34, y+16, fill="#fff")
        # Leg animation
        if self.dino_on_ground:
            leg_offset = 10 if (self.dino_frame // 4) % 2 == 0 else -10
            self.canvas.create_line(x+10, y+40, x+10, y+55, fill="#535353", width=4)
            self.canvas.create_line(x+30, y+40, x+30+leg_offset, y+55, fill="#535353", width=4)
        else:
            self.canvas.create_line(x+10, y+40, x+5, y+50, fill="#535353", width=4)
            self.canvas.create_line(x+30, y+40, x+35, y+50, fill="#535353", width=4)
        # Arm
        self.canvas.create_line(x+5, y+20, x-5, y+30, fill="#535353", width=3)
    
    def draw_obstacle(self, obs):
        x, y, w, h, type_ = obs
        if type_ == "cactus":
            # Cactus body
            self.canvas.create_rectangle(x+15, y, x+25, y+h, fill="#6b8e23", outline="#556b2f")
            # Arms
            self.canvas.create_rectangle(x, y+15, x+15, y+25, fill="#6b8e23", outline="#556b2f")
            self.canvas.create_rectangle(x+25, y+30, x+40, y+40, fill="#6b8e23", outline="#556b2f")
        elif type_ == "bird":
            wing = 5 if (self.dino_frame // 3) % 2 == 0 else -5
            self.canvas.create_oval(x, y+wing, x+40, y+20+wing, fill="#535353", outline="#535353")
            self.canvas.create_oval(x+10, y+5+wing, x+18, y+13+wing, fill="#fff")
    
    def on_space(self, event):
        if not self.running and not self.game_over:
            self.start_game()
        elif self.running and self.dino_on_ground:
            self.dino_vel_y = self.jump_power
            self.dino_on_ground = False
    
    def on_down(self, event):
        if self.running and not self.dino_on_ground:
            self.dino_vel_y = abs(self.dino_vel_y) + 5
    
    def start_game(self):
        self.running = True
        self.game_over = False
        self.score = 0
        self.speed = 8
        self.obstacles = []
        self.dino_y = 220
        self.dino_vel_y = 0
        self.dino_on_ground = True
        self.status_label.config(text="")
        self.score_label.config(text=f"Score: {self.score}  |  HI: {self.high_score}")
    
    def restart(self, event):
        if self.game_over:
            self.start_game()
    
    def spawn_obstacle(self):
        if random.random() < 0.02:
            type_ = "cactus" if random.random() < 0.7 else "bird"
            if type_ == "cactus":
                h = random.choice([40, 50, 60])
                self.obstacles.append([800, 250-h, 40, h, "cactus"])
            else:
                y = random.choice([160, 190, 220])
                self.obstacles.append([800, y, 40, 20, "bird"])
    
    def update_dino(self):
        self.dino_vel_y += self.gravity
        self.dino_y += self.dino_vel_y
        
        if self.dino_y >= 220:
            self.dino_y = 220
            self.dino_vel_y = 0
            self.dino_on_ground = True
        else:
            self.dino_on_ground = False
        
        self.dino_frame += 1
    
    def update_obstacles(self):
        for obs in self.obstacles[:]:
            obs[0] -= self.speed
            if obs[0] < -50:
                self.obstacles.remove(obs)
                self.score += 1
                if self.score > self.high_score:
                    self.high_score = self.score
                self.score_label.config(text=f"Score: {self.score}  |  HI: {self.high_score}")
                
                # Increase speed every 50 points
                if self.score % 50 == 0:
                    self.speed = min(20, self.speed + 0.5)
            
            # Collision detection
            if self.check_collision(obs):
                self.game_over = True
                self.running = False
                self.status_label.config(text=f"GAME OVER! Score: {self.score}  |  Press R to restart")
    
    def check_collision(self, obs):
        ox, oy, ow, oh, _ = obs
        dx, dy = self.dino_x, self.dino_y
        dw, dh = 40, 40
        
        # Shrink hitbox slightly for fairness
        return not (dx + 5 > ox + ow - 5 or dx + dw - 5 < ox + 5 or 
                    dy + 5 > oy + oh - 5 or dy + dh - 5 < oy + 5)
    
    def update_clouds(self):
        for cloud in self.clouds:
            cloud[0] -= cloud[2]
            if cloud[0] < -60:
                cloud[0] = 860
                cloud[1] = random.randint(30, 120)
    
    def game_loop(self):
        if self.running:
            self.update_dino()
            self.update_obstacles()
            self.spawn_obstacle()
            self.update_clouds()
        
        self.draw_static()
        self.root.after(16, self.game_loop)  # ~60 FPS

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.after(100, lambda: root.attributes('-topmost', False))
    app = DinoGame(root)
    root.mainloop()