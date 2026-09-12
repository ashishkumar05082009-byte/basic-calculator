import tkinter as tk
import random

class DinoGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Chrome Dino")
        self.root.geometry("800x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        self.canvas = tk.Canvas(root, width=800, height=300, bg="#f0f0f0", highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Game state
        self.running = False
        self.game_over = False
        self.score = 0
        self.high_score = 0
        self.speed = 6
        self.gravity = 1.2
        self.jump_power = -18
        self.dino_y = 220
        self.dino_vel_y = 0
        self.dino_on_ground = True
        self.dino_frame = 0
        self.obstacles = []
        self.ground_x = 0
        
        # UI
        self.score_label = tk.Label(root, text="0", font=("Arial", 24, "bold"), 
                                     fg="#333", bg="#f0f0f0")
        self.score_label.pack()
        
        self.status_label = tk.Label(root, text="Press SPACE to Start", font=("Arial", 14), 
                                      fg="#666", bg="#f0f0f0")
        self.status_label.pack(pady=10)
        
        # Bind controls
        self.root.bind("<space>", self.on_space)
        self.root.bind("<Up>", self.on_space)
        self.root.bind("<r>", self.restart)
        self.root.focus_set()
        
        # Ground elements
        self.ground_items = []
        
        # Dino animation frames
        self.dino_frames_run = []
        self.dino_frames_jump = []
        self.dino_frames_duck = []
        self.load_assets()
        
        self.draw_start_screen()
        self.root.after(100, self.game_loop)
    
    def load_assets(self):
        # Simple colored shapes instead of images for reliability
        # Dino body colors
        self.dino_body = "#535353"
        self.dino_dark = "#333333"
        self.dino_light = "#777777"
        
        # Create simple dino shapes that will be drawn differently each frame
        # We'll just draw primitives each frame
    
    def draw_start_screen(self):
        self.canvas.delete("all")
        self.canvas.create_text(400, 150, text="🦕 CHROME DINO 🦕", 
                                 font=("Arial", 36, "bold"), fill="#535353")
        self.canvas.create_text(400, 220, text="Press SPACE to Start", 
                                 font=("Arial", 18), fill="#666666")
        self.canvas.create_text(400, 280, text="Avoid obstacles and survive!", 
                                 font=("Arial", 14), fill="#999999")
        self.canvas.create_text(400, 350, text="High Score: 0", 
                                 font=("Arial", 12), fill="#bbbbbb")
    
    def on_space(self, event):
        if not self.running and not self.game_over:
            self.start_game()
        elif self.running and self.dino_on_ground:
            self.dino_vel_y = self.jump_power
            self.dino_on_ground = False
    
    def on_restart(self, event):
        if self.game_over:
            self.start_game()
    
    def start_game(self):
        self.running = True
        self.game_over = False
        self.score = 0
        self.speed = 6
        self.dino_y = 220
        self.dino_vel_y = 0
        self.dino_on_ground = True
        self.obstacles = []
        self.ground_x = 0
        self.status_label.config(text="")
        self.score_label.config(text="0")
        self.draw_game()
    
    def restart(self, event):
        if self.game_over:
            self.start_game()
    
    def draw_game(self):
        self.canvas.delete("all")
        
        # Draw horizon line
        self.canvas.create_line(0, 250, 800, 250, fill="#dddddd", width=1)
        
        # Draw ground pattern
        for i in range(-int(self.ground_x % 40), 800, 40):
            self.canvas.create_rectangle(i, 270, i+20, 300, fill="#c0c0c0", outline="")
        self.ground_x += self.speed
        
        # Draw obstacles
        for obs in self.obstacles:
            self.draw_obstacle(obs)
        
        # Draw dino
        self.draw_dino()
        
        # Draw score
        self.canvas.create_text(700, 40, text=f"Score: {self.score}", 
                                 font=("Arial", 18, "bold"), fill="#333333")
    
    def draw_obstacle(self, obs):
        obs_type = obs['type']
        x, y = obs['x'], obs['y']
        w, h = obs['w'], obs['h']
        
        if obs_type == 'cactus':
            # Main body
            self.canvas.create_rectangle(x + 15, y, x + 25, y + h, fill="#6b8e23", outline="#556b2f")
            # Arms
            self.canvas.create_rectangle(x, y + 15, x + 15, y + 25, fill="#6b8e23", outline="#556b2f")
            self.canvas.create_rectangle(x + 25, y + 30, x + 40, y + 40, fill="#6b8e23", outline="#556b2f")
        elif obs_type == 'bird':
            # Bird body
            self.canvas.create_oval(x, y + 5, x + 40, y + 25, fill="#535353", outline="#333333")
            # Eye
            self.canvas.create_oval(x + 32, y + 8, x + 38, y + 14, fill="#fff")
            # Wing
            self.canvas.create_oval(x + 10, y + 12, x + 18, y + 18, fill="#535353")
    
    def draw_dino(self):
        x = 80
        y = self.dino_y
        frame = (self.dino_frame // 3) % 4
        
        if not self.dino_on_ground and self.dino_vel_y < 0:
            # Jumping up
            self.canvas.create_oval(x + 8, y + 12, x + 40, y + 38, fill="#535353", outline="#333333")
            self.canvas.create_oval(x + 28, y + 8, x + 34, y + 14, fill="#fff")
            # Arms up
            self.canvas.create_line(x + 8, y + 20, x + 4, y + 12, fill="#535353", width=3)
            self.canvas.create_line(x + 36, y + 20, x + 40, y + 12, fill="#535353", width=3)
        elif not self.dino_on_ground and self.dino_vel_y > 0:
            # Falling down
            self.canvas.create_oval(x + 8, y + 12, x + 40, y + 38, fill="#535353", outline="#333333")
            self.canvas.create_oval(x + 28, y + 8, x + 34, y + 14, fill="#fff")
            # Arms down
            self.canvas.create_line(x + 8, y + 20, x + 4, y + 28, fill="#535353", width=3)
            self.canvas.create_line(x + 36, y + 20, x + 40, y + 28, fill="#535353", width=3)
        elif frame == 0:
            # Running frame 1
            self.canvas.create_oval(x + 6, y + 10, x + 42, y + 36, fill="#535353", outline="#333333")
            self.canvas.create_oval(x + 28, y + 4, x + 34, y + 10, fill="#fff")
            # Legs
            self.canvas.create_line(x + 12, y + 44, x + 8, y + 58, fill="#535353", width=4)
            self.canvas.create_line(x + 32, y + 44, x + 40, y + 58, fill="#535353", width=4)
            # Arms
            self.canvas.create_line(x + 6, y + 22, x - 2, y + 30, fill="#535353", width=3)
            self.canvas.create_line(x + 16, y + 22, x + 6, y + 30, fill="#535353", width=3)
        elif frame == 1:
            # Running frame 2
            self.canvas.create_oval(x + 8, y + 10, x + 44, y + 36, fill="#535353", outline="#333333")
            self.canvas.create_oval(x + 30, y + 4, x + 36, y + 10, fill="#fff")
            # Legs switched
            self.canvas.create_line(x + 12, y + 44, x + 14, y + 58, fill="#535353", width=4)
            self.canvas.create_line(x + 32, y + 44, x + 36, y + 58, fill="#535353", width=4)
            # Arms
            self.canvas.create_line(x + 8, y + 22, x + 2, y + 30, fill="#535353", width=3)
            self.canvas.create_line(x + 18, y + 22, x + 10, y + 30, fill="#535353", width=3)
        elif frame == 2:
            # Running frame 3
            self.canvas.create_oval(x + 6, y + 12, x + 42, y + 38, fill="#535353", outline="#333333")
            self.canvas.create_oval(x + 26, y + 6, x + 32, y + 12, fill="#fff")
            # Legs
            self.canvas.create_line(x + 10, y + 44, x + 6, y + 58, fill="#535353", width=4)
            self.canvas.create_line(x + 34, y + 44, x + 38, y + 58, fill="#535353", width=4)
            # Arms
            self.canvas.create_line(x + 4, y + 22, x - 2, y + 30, fill="#535353", width=3)
            self.canvas.create_line(x + 14, y + 22, x + 4, y + 30, fill="#535353", width=3)
        else:
            # Running frame 4
            self.canvas.create_oval(x + 8, y + 12, x + 44, y + 38, fill="#535353", outline="#333333")
            self.canvas.create_oval(x + 30, y + 4, x + 36, y + 10, fill="#fff")
            # Legs switched again
            self.canvas.create_line(x + 12, y + 44, x + 16, y + 58, fill="#535353", width=4)
            self.canvas.create_line(x + 32, y + 44, x + 38, y + 58, fill="#535353", width=4)
            # Arms
            self.canvas.create_line(x + 6, y + 22, x + 2, y + 30, fill="#535353", width=3)
            self.canvas.create_line(x + 18, y + 22, x + 12, y + 30, fill="#535353", width=3)
        
        # Eye
        self.canvas.create_oval(x + 38, y + 10, x + 44, y + 16, fill="#333333")
        # Nostril
        self.canvas.create_oval(x + 44, y + 4, x + 46, y + 6, fill="#333333")
    
    def update_dino(self):
        if not self.dino_on_ground:
            self.dino_vel_y += self.gravity
            self.dino_y += self.dino_vel_y
            
            if self.dino_y >= 220:
                self.dino_y = 220
                self.dino_vel_y = 0
                self.dino_on_ground = True
        
        self.dino_frame += 1
    
    def spawn_obstacle(self):
        if random.random() < 0.015:
            if random.random() < 0.6:
                # Cactus
                h = random.choice([45, 55, 65])
                self.obstacles.append({'x': 800, 'y': 220 - h, 'w': 35, 'h': h, 'type': 'cactus'})
            else:
                # Bird
                y_pos = random.choice([180, 210, 240])
                self.obstacles.append({'x': 800, 'y': y_pos, 'w': 40, 'h': 25, 'type': 'bird'})
    
    def update_obstacles(self):
        for obs in self.obstacles[:]:
            obs['x'] -= self.speed
            
            # Collision detection
            dx, dy = 80, self.dino_y
            dw, dh = 44, 48
            ox, oy, ow, oh = obs['x'], obs['y'], obs['w'], obs['h']
            
            # Check collision with padding
            if (dx + 5 < ox + ow - 5 and dx + dw - 5 > ox + 5 and
                dy + 5 < oy + oh - 5 and dy + dh - 5 > oy + 5):
                self.game_over_func()
            
            if obs['x'] < -50:
                self.obstacles.remove(obs)
                self.score += 1
                if self.score > self.high_score:
                    self.high_score = self.score
        
        # Increase speed every 100 points
        if self.score > 0 and self.score % 100 == 0:
            self.speed = min(15, self.speed + 0.5)
    
    def game_over_func(self):
        self.running = False
        self.game_over = True
        if self.score > self.high_score:
            self.high_score = self.score
        self.score_label.config(text=f"HI {self.high_score}")
        self.canvas.create_text(400, 150, text="GAME OVER", 
                                 font=("Arial", 36, "bold"), fill="#ff5252")
        self.canvas.create_text(400, 220, text=f"Final Score: {self.score}", 
                                 font=("Arial", 24), fill="#333333")
        self.canvas.create_text(400, 280, text="Press R to Restart", 
                                 font=("Arial", 18), fill="#666666")
    
    def game_loop(self):
        if self.running:
            self.update_dino()
            self.spawn_obstacle()
            self.update_obstacles()
        
        self.draw_game()
        self.root.after(16, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.after(100, lambda: root.attributes('-topmost', False))
    game = DinoGame(root)
    root.mainloop()