import tkinter as tk
from tkinter import ttk, messagebox
import heapq

# Punjab district road network
# Distances are illustrative, not verified real road distances.

GRAPH = {
    "Amritsar": {
        "Tarn Taran": 25, "Gurdaspur": 75, "Kapurthala": 70
    },
    "Barnala": {
        "Sangrur": 40, "Moga": 65, "Bathinda": 85,
        "Ludhiana": 80, "Malerkotla": 45
    },
    "Bathinda": {
        "Mansa": 65, "Faridkot": 65, "Sri Muktsar Sahib": 55,
        "Barnala": 85
    },
    "Faridkot": {
        "Moga": 45, "Bathinda": 65, "Ferozepur": 70
    },
    "Fatehgarh Sahib": {
        "Patiala": 45, "Ludhiana": 70, "Rupnagar": 65,
        "Malerkotla": 65
    },
    "Fazilka": {
        "Sri Muktsar Sahib": 65, "Ferozepur": 90
    },
    "Ferozepur": {
        "Faridkot": 70, "Moga": 85, "Fazilka": 90
    },
    "Gurdaspur": {
        "Pathankot": 35, "Hoshiarpur": 75, "Amritsar": 75
    },
    "Hoshiarpur": {
        "Jalandhar": 45, "Gurdaspur": 75, "Pathankot": 85,
        "SBS Nagar": 65
    },
    "Jalandhar": {
        "Kapurthala": 25, "Hoshiarpur": 45,
        "Ludhiana": 60, "SBS Nagar": 50
    },
    "Kapurthala": {
        "Jalandhar": 25, "Amritsar": 70, "Tarn Taran": 65
    },
    "Ludhiana": {
        "Jalandhar": 60, "Barnala": 80, "Fatehgarh Sahib": 70,
        "SBS Nagar": 70, "Malerkotla": 55
    },
    "Malerkotla": {
        "Sangrur": 30, "Barnala": 45, "Ludhiana": 55,
        "Fatehgarh Sahib": 65
    },
    "Mansa": {
        "Bathinda": 65, "Sangrur": 70, "Patiala": 110
    },
    "Moga": {
        "Barnala": 65, "Faridkot": 45, "Ferozepur": 85,
        "Ludhiana": 75
    },
    "Pathankot": {
        "Gurdaspur": 35, "Hoshiarpur": 85
    },
    "Patiala": {
        "Fatehgarh Sahib": 45, "Sangrur": 65,
        "Mansa": 110, "SAS Nagar": 70
    },
    "Rupnagar": {
        "Fatehgarh Sahib": 65, "SAS Nagar": 45,
        "SBS Nagar": 55, "Hoshiarpur": 75
    },
    "SAS Nagar": {
        "Patiala": 70, "Rupnagar": 45
    },
    "SBS Nagar": {
        "Jalandhar": 50, "Hoshiarpur": 65,
        "Ludhiana": 70, "Rupnagar": 55
    },
    "Sangrur": {
        "Barnala": 40, "Malerkotla": 30,
        "Patiala": 65, "Mansa": 70
    },
    "Sri Muktsar Sahib": {
        "Bathinda": 55, "Fazilka": 65
    },
    "Tarn Taran": {
        "Amritsar": 25, "Kapurthala": 65
    }
}


# Dijkstra's shortest path algorithm
def dijkstra(graph, start, destination):
    distances = {district: float("inf") for district in graph}
    previous = {district: None for district in graph}

    distances[start] = 0
    queue = [(0, start)]

    while queue:
        current_distance, current = heapq.heappop(queue)

        if current_distance > distances[current]:
            continue

        if current == destination:
            break

        for neighbour, weight in graph[current].items():
            new_distance = current_distance + weight

            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous[neighbour] = current

                heapq.heappush(
                    queue, (new_distance, neighbour)
                )

    if distances[destination] == float("inf"):
        return None, []

    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    return distances[destination], path


# GUI application
class ShortestPathApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Punjab District Shortest Path Finder")
        self.root.geometry("850x620")
        self.root.minsize(700, 550)
        self.root.configure(bg="#f1f5f9")

        self.blue = "#1d4ed8"
        self.dark = "#172554"
        self.green = "#15803d"

        self.create_ui()

    def create_ui(self):
        # Header
        header = tk.Frame(
            self.root, bg=self.dark, padx=25, pady=22
        )
        header.pack(fill="x")

        tk.Label(
            header,
            text="PUNJAB DISTRICT SHORTEST PATH FINDER",
            font=("Arial", 19, "bold"),
            bg=self.dark,
            fg="white"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="DAA Mini Project | Dijkstra's Algorithm",
            font=("Arial", 11),
            bg=self.dark,
            fg="#cbd5e1"
        ).pack(anchor="w", pady=(6, 0))

        # Main content
        body = tk.Frame(
            self.root, bg="#f1f5f9", padx=25, pady=22
        )
        body.pack(fill="both", expand=True)

        tk.Label(
            body,
            text="Find the shortest route",
            font=("Arial", 16, "bold"),
            bg="#f1f5f9",
            fg=self.dark
        ).pack(anchor="w")

        tk.Label(
            body,
            text="Choose your starting and destination districts.",
            font=("Arial", 10),
            bg="#f1f5f9",
            fg="#64748b"
        ).pack(anchor="w", pady=(5, 15))

        # Selection card
        card = tk.Frame(
            body, bg="white", padx=18, pady=18
        )
        card.pack(fill="x")

        districts = sorted(GRAPH.keys())

        tk.Label(
            card,
            text="STARTING DISTRICT",
            bg="white",
            fg="#475569",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, sticky="w", padx=5)

        tk.Label(
            card,
            text="DESTINATION DISTRICT",
            bg="white",
            fg="#475569",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=1, sticky="w", padx=5)

        self.start = tk.StringVar(value="Jalandhar")
        self.end = tk.StringVar(value="Amritsar")

        self.start_box = ttk.Combobox(
            card,
            textvariable=self.start,
            values=districts,
            state="readonly",
            width=24,
            font=("Arial", 11)
        )
        self.start_box.grid(
            row=1, column=0, padx=5,
            pady=(8, 0), sticky="ew"
        )

        self.end_box = ttk.Combobox(
            card,
            textvariable=self.end,
            values=districts,
            state="readonly",
            width=24,
            font=("Arial", 11)
        )
        self.end_box.grid(
            row=1, column=1, padx=5,
            pady=(8, 0), sticky="ew"
        )

        card.columnconfigure(0, weight=1)
        card.columnconfigure(1, weight=1)

        tk.Button(
            card,
            text="FIND SHORTEST PATH",
            command=self.find_path,
            bg=self.blue,
            fg="white",
            activebackground="#1e40af",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=15,
            pady=10,
            cursor="hand2"
        ).grid(
            row=2, column=0, columnspan=2,
            sticky="ew", padx=5, pady=(15, 0)
        )

        # Results card
        result = tk.Frame(
            body, bg="white", padx=18, pady=18
        )
        result.pack(fill="both", expand=True, pady=(18, 0))

        tk.Label(
            result,
            text="SHORTEST DISTANCE",
            bg="white",
            fg="#64748b",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.distance_label = tk.Label(
            result,
            text="— km",
            bg="white",
            fg=self.green,
            font=("Arial", 27, "bold")
        )
        self.distance_label.pack(anchor="w", pady=(3, 10))

        self.route_label = tk.Label(
            result,
            text="Your route will appear here.",
            bg="white",
            fg=self.dark,
            font=("Arial", 11, "bold")
        )
        self.route_label.pack(anchor="w", pady=(0, 8))

        self.output = tk.Text(
            result,
            height=7,
            wrap="word",
            font=("Arial", 11),
            bg="#f8fafc",
            fg="#1e293b",
            relief="flat",
            padx=10,
            pady=10
        )
        self.output.pack(fill="both", expand=True)
        self.output.config(state="disabled")

        tk.Label(
            body,
            text=(
                "Note: Distances are illustrative sample data, "
                "not verified real-world road distances."
            ),
            bg="#f1f5f9",
            fg="#9a3412",
            font=("Arial", 9),
            wraplength=780
        ).pack(anchor="w", pady=(10, 0))

        self.find_path()

    def find_path(self):
        start = self.start.get()
        destination = self.end.get()

        distance, path = dijkstra(
            GRAPH, start, destination
        )

        if not path:
            messagebox.showerror(
                "No route",
                "No route found in this sample network."
            )
            return

        self.distance_label.config(text=f"{distance} km")
        self.route_label.config(
            text=f"{start}  →  {destination}"
        )

        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)

        self.output.insert(
            tk.END, "SHORTEST ROUTE\n\n"
        )
        self.output.insert(
            tk.END, "  →  ".join(path) + "\n\n"
        )
        self.output.insert(
            tk.END, "ROUTE DETAILS\n\n"
        )

        for i in range(len(path) - 1):
            a = path[i]
            b = path[i + 1]
            km = GRAPH[a][b]

            self.output.insert(
                tk.END, f"{a} to {b}: {km} km\n"
            )

        if len(path) == 1:
            self.output.insert(
                tk.END,
                "Start and destination are the same district.\n"
            )

        self.output.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = ShortestPathApp(root)
    root.mainloop()