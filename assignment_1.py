import heapq
import math
import time

def a_star_search(graph, distances, start, goal):
    """
    Implementasi algoritma A* untuk menemukan jalur terpendek antara dua kota
    
    Args:
        graph: Dictionary ketetanggaan antar kota
        distances: Dictionary koordinat tiap kota
        start: Kota awal
        goal: Kota tujuan
    
    Returns:
        path: Jalur terpendek yang ditemukan
        visited_count: Jumlah node yang dikunjungi
        time_taken: Waktu eksekusi dalam milidetik
    """
    # Fungsi heuristik - menggunakan jarak Euclidean
    def heuristic(node):
        x1, y1 = distances[node]
        x2, y2 = distances[goal]
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    # Mencatat waktu mulai
    start_time = time.time()
    
    # Menyiapkan struktur data untuk algoritma A*
    open_set = []  # Priority queue
    closed_set = set()
    visited_count = 0
    
    # Format: (f_score, city, path, g_score)
    # f_score = g_score + heuristic
    heapq.heappush(open_set, (heuristic(start), start, [start], 0))
    
    while open_set:
        # Mengambil node dengan f_score terkecil
        f, current, path, g_score = heapq.heappop(open_set)
        visited_count += 1
        
        # Jika tujuan sudah ditemukan, kembalikan hasilnya
        if current == goal:
            time_taken = (time.time() - start_time) * 1000  # Konversi ke milidetik
            return path, visited_count, time_taken
        
        # Tandai node saat ini sebagai sudah dikunjungi
        if current in closed_set:
            continue
        closed_set.add(current)
        
        # Jelajahi semua tetangga dari node saat ini
        for neighbor in graph.get(current, []):
            if neighbor in closed_set:
                continue
            
            # Hitung jarak antar kota
            x1, y1 = distances[current]
            x2, y2 = distances[neighbor]
            edge_cost = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            
            # Hitung skor baru
            new_g_score = g_score + edge_cost
            new_f_score = new_g_score + heuristic(neighbor)
            
            # Tambahkan ke open set
            heapq.heappush(open_set, (new_f_score, neighbor, path + [neighbor], new_g_score))
    
    # Jika tidak ada jalur yang ditemukan
    time_taken = (time.time() - start_time) * 1000  # Konversi ke milidetik
    return None, visited_count, time_taken

def greedy_best_first_search(graph, distances, start, goal):
    """
    Implementasi algoritma Greedy Best-First Search untuk menemukan jalur antara dua kota
    
    Args:
        graph: Dictionary ketetanggaan antar kota
        distances: Dictionary koordinat tiap kota
        start: Kota awal
        goal: Kota tujuan
    
    Returns:
        path: Jalur yang ditemukan
        visited_count: Jumlah node yang dikunjungi
        time_taken: Waktu eksekusi dalam milidetik
    """
    # Fungsi heuristik - menggunakan jarak Euclidean
    def heuristic(node):
        x1, y1 = distances[node]
        x2, y2 = distances[goal]
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    # Mencatat waktu mulai
    start_time = time.time()
    
    # Menyiapkan struktur data
    open_set = []  # Priority queue
    closed_set = set()
    visited_count = 0
    
    # Format: (heuristic_score, city, path)
    heapq.heappush(open_set, (heuristic(start), start, [start]))
    
    while open_set:
        # Mengambil node dengan skor heuristik terkecil
        h, current, path = heapq.heappop(open_set)
        visited_count += 1
        
        # Jika tujuan sudah ditemukan, kembalikan hasilnya
        if current == goal:
            time_taken = (time.time() - start_time) * 1000  # Konversi ke milidetik
            return path, visited_count, time_taken
        
        # Tandai node saat ini sebagai sudah dikunjungi
        if current in closed_set:
            continue
        closed_set.add(current)
        
        # Jelajahi semua tetangga dari node saat ini
        for neighbor in graph.get(current, []):
            if neighbor in closed_set:
                continue
            
            # Tambahkan ke open set
            heapq.heappush(open_set, (heuristic(neighbor), neighbor, path + [neighbor]))
    
    # Jika tidak ada jalur yang ditemukan
    time_taken = (time.time() - start_time) * 1000  # Konversi ke milidetik
    return None, visited_count, time_taken

# Contoh penggunaan
if __name__ == "__main__":
    # Data kota dan jalan
    cities = {
        "A": (0, 0),
        "B": (2, 1),
        "C": (4, 2),
        "D": (5, 5),
        "E": (1, 4)
    }
    
    roads = {
        "A": ["B", "E"],
        "B": ["A", "C"],
        "C": ["B", "D"],
        "D": ["C"],
        "E": ["A", "D"]
    }
    
    # Menjalankan algoritma A*
    start_city = "A"
    goal_city = "D"
    
    print(f"Mencari rute dari {start_city} ke {goal_city}:")
    
    # A* Search
    a_star_path, a_star_visited, a_star_time = a_star_search(roads, cities, start_city, goal_city)
    print("\nA* Search:")
    print(f"Jalur: {' -> '.join(a_star_path)}")
    print(f"Jumlah node yang dikunjungi: {a_star_visited}")
    print(f"Waktu eksekusi: {a_star_time:.2f} ms")
    
    # Greedy Best-First Search
    gbfs_path, gbfs_visited, gbfs_time = greedy_best_first_search(roads, cities, start_city, goal_city)
    print("\nGreedy Best-First Search:")
    print(f"Jalur: {' -> '.join(gbfs_path)}")
    print(f"Jumlah node yang dikunjungi: {gbfs_visited}")
    print(f"Waktu eksekusi: {gbfs_time:.2f} ms")
    
    # Visualisasi sederhana dari rute
    def visualize_map(cities, path):
        # Tentukan ukuran peta
        max_x = max(x for x, y in cities.values()) + 1
        max_y = max(y for x, y in cities.values()) + 1
        
        # Buat peta kosong
        grid = [[' ' for _ in range(max_x * 2 + 1)] for _ in range(max_y * 2 + 1)]
        
        # Tandai kota-kota
        for city, (x, y) in cities.items():
            grid[y * 2][x * 2] = city
        
        # Tandai rute
        for i in range(len(path) - 1):
            city1, city2 = path[i], path[i + 1]
            x1, y1 = cities[city1]
            x2, y2 = cities[city2]
            
            # Menandai jalan dengan '*'
            if x1 == x2:  # Vertikal
                for y in range(min(y1, y2) * 2, max(y1, y2) * 2 + 1):
                    if grid[y][x1 * 2] == ' ':
                        grid[y][x1 * 2] = '*'
            elif y1 == y2:  # Horizontal
                for x in range(min(x1, x2) * 2, max(x1, x2) * 2 + 1):
                    if grid[y1 * 2][x] == ' ':
                        grid[y1 * 2][x] = '*'
            else:  # Diagonal
                # Implementasi sederhana untuk diagonal
                steps = max(abs(x2 - x1), abs(y2 - y1))
                for step in range(1, steps):
                    x = int(x1 * 2 + (x2 - x1) * 2 * step / steps)
                    y = int(y1 * 2 + (y2 - y1) * 2 * step / steps)
                    if grid[y][x] == ' ':
                        grid[y][x] = '*'
        
        # Cetak peta
        for row in grid:
            print(''.join(row))
    
    print("\nVisualisasi Rute A*:")
    visualize_map(cities, a_star_path)
    
    print("\nVisualisasi Rute GBFS:")
    visualize_map(cities, gbfs_path)