import tkinter as tk
from tkinter import messagebox
import networkx as nx
import random

class SafePathFinderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ Disaster Rescue: Safe Path Finder")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e2e")

        self.graph = nx.Graph()
        self.node_positions = {}

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="🚨 Disaster Safe Path Finder 🚨", font=("Helvetica", 18, "bold"),
                         fg="white", bg="#1e1e2e")
        title.pack(pady=10)

        # Frame for inputs
        control_frame = tk.Frame(self.root, bg="#1e1e2e")
        control_frame.pack(pady=10)

        self.entry_path = tk.Entry(control_frame, width=30)
        self.entry_path.grid(row=0, column=0, padx=5)
        self.entry_path.insert(0, "A-B-10")

        tk.Button(control_frame, text="➕ Add Path", command=self.add_path, bg="#4CAF50", fg="white").grid(row=0, column=1)

        self.entry_block = tk.Entry(control_frame, width=20)
        self.entry_block.grid(row=1, column=0, pady=5)
        self.entry_block.insert(0, "A-B")

        tk.Button(control_frame, text="⛔ Block Road", command=self.block_road, bg="#f44336", fg="white").grid(row=1, column=1)

        self.entry_start = tk.Entry(control_frame, width=10)
        self.entry_start.grid(row=2, column=0)
        self.entry_start.insert(0, "Start")

        self.entry_end = tk.Entry(control_frame, width=10)
        self.entry_end.grid(row=2, column=1)
        self.entry_end.insert(0, "End")

        tk.Button(control_frame, text="🚀 Find Path", command=self.find_path, bg="#2196F3", fg="white").grid(row=2, column=2, padx=5)

        # Canvas Map View
        self.canvas = tk.Canvas(self.root, width=700, height=400, bg="white")
        self.canvas.pack(pady=20)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def add_path(self):
        try:
            data = self.entry_path.get().split("-")
            u, v, w = data[0].strip(), data[1].strip(), int(data[2].strip())
            self.graph.add_edge(u, v, weight=w)

            # Assign random positions to new nodes
            if u not in self.node_positions:
                self.node_positions[u] = (random.randint(50, 650), random.randint(50, 350))
            if v not in self.node_positions:
                self.node_positions[v] = (random.randint(50, 650), random.randint(50, 350))

            self.draw_graph()
            messagebox.showinfo("Success", f"✅ Path added: {u} ↔ {v} (Distance: {w})")
        except:
            messagebox.showerror("Error", "❗ Enter valid input: A-B-Distance")

    def block_road(self):
        try:
            data = self.entry_block.get().split("-")
            u, v = data[0].strip(), data[1].strip()
            if self.graph.has_edge(u, v):
                self.graph.remove_edge(u, v)
                self.draw_graph()
                messagebox.showinfo("Blocked", f"🚫 Road blocked between {u} and {v}")
            else:
                messagebox.showwarning("Warning", "❗ Road does not exist!")
        except:
            messagebox.showerror("Error", "Invalid input for blocking road.")

    def find_path(self):
        start = self.entry_start.get().strip()
        end = self.entry_end.get().strip()
        try:
            path = nx.dijkstra_path(self.graph, start, end, weight='weight')
            distance = nx.dijkstra_path_length(self.graph, start, end, weight='weight')
            messagebox.showinfo("Path Found ✅", f"Path: {' → '.join(path)}\nDistance: {distance}")
            self.draw_graph(path)
        except nx.NetworkXNoPath:
            messagebox.showerror("❌ No Path", "No safe path found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def draw_graph(self, highlight_path=[]):
        self.canvas.delete("all")

        for node, (x, y) in self.node_positions.items():
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="#ffc107", outline="black")
            self.canvas.create_text(x, y, text=node, font=("Arial", 12, "bold"))

        for u, v in self.graph.edges():
            x1, y1 = self.node_positions[u]
            x2, y2 = self.node_positions[v]
            color = "red" if (u in highlight_path and v in highlight_path) and \
                           (highlight_path.index(v) == highlight_path.index(u)+1 or highlight_path.index(u) == highlight_path.index(v)+1) else "gray"
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=3 if color == "red" else 1)
            weight = self.graph[u][v]['weight']
            mx, my = (x1+x2)//2, (y1+y2)//2
            self.canvas.create_text(mx, my, text=str(weight), fill="blue", font=("Arial", 10, "bold"))

    def on_canvas_click(self, event):
        clicked = None
        for node, (x, y) in self.node_positions.items():
            if abs(event.x - x) < 20 and abs(event.y - y) < 20:
                clicked = node
                break

        if clicked:
            current_start = self.entry_start.get()
            if current_start == "Start" or current_start == "":
                self.entry_start.delete(0, tk.END)
                self.entry_start.insert(0, clicked)
            else:
                self.entry_end.delete(0, tk.END)
                self.entry_end.insert(0, clicked)

if __name__ == "__main__":
    root = tk.Tk()
    app = SafePathFinderGUI(root)
    root.mainloop()
