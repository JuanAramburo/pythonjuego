import tkinter as tk
import random

WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20

# Posiciones iniciales
player_pos = [1, 1]
obstacles = []
enemies = []
goal = (28, 28)
game_over = False

# Algoritmo A* para encontrar la ruta
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Movimiento de enemigos (Minimax simplificado)
def enemy_move(enemy_pos, player_pos, obstacles):
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    best_move = enemy_pos
    best_distance = float('inf')

    for move in moves:
        new_pos = (enemy_pos[0] + move[0], enemy_pos[1] + move[1])
        if new_pos not in obstacles and 0 <= new_pos[0] < 30 and 0 <= new_pos[1] < 30:
            distance = heuristic(new_pos, player_pos)
            if distance < best_distance:
                best_distance = distance
                best_move = new_pos

    return best_move

# Movimiento del jugador
def move_player(dx, dy):
    global player_pos, game_over
    if game_over:
        return
    new_pos = (player_pos[0] + dx, player_pos[1] + dy)
    if new_pos not in obstacles and 0 <= new_pos[0] < 30 and 0 <= new_pos[1] < 30:
        player_pos[0] += dx
        player_pos[1] += dy
    if tuple(player_pos) == goal:
        end_game("¡Has llegado a la meta!")
    elif tuple(player_pos) in enemies:
        end_game("¡Te atrapó un enemigo!")
    update_canvas()

# Actualizar el lienzo
def update_canvas():
    global game_over
    canvas.delete("all")

    # Dibujar obstáculos
    for x, y in obstacles:
        canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill="red")

    # Dibujar enemigos si el juego no ha terminado
    if not game_over:
        for i in range(len(enemies)):
            enemies[i] = enemy_move(enemies[i], tuple(player_pos), obstacles)
            x, y = enemies[i]
            canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill="purple")

    # Dibujar jugador
    x, y = player_pos
    canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill="black")

    # Dibujar meta
    gx, gy = goal
    canvas.create_rectangle(gx * CELL_SIZE, gy * CELL_SIZE, (gx + 1) * CELL_SIZE, (gy + 1) * CELL_SIZE, fill="blue")

# Iniciar el juego
def start_game():
    global player_pos, obstacles, enemies, game_over
    player_pos = [1, 1]
    obstacles = [(random.randint(1, 29), random.randint(1, 29)) for _ in range(40)]
    enemies = [(random.randint(1, 29), random.randint(1, 29)) for _ in range(3)]
    game_over = False
    update_canvas()

# Terminar el juego
def end_game(message):
    global game_over
    game_over = True
    canvas.delete("all")
    canvas.create_text(WIDTH // 2, HEIGHT // 2, text=message, font=("Arial", 24), fill="black")

# Configuración de la ventana
root = tk.Tk()
root.title("Carrera con Obstáculos - Tkinter")

# Menú de inicio
menu = tk.Menu(root)
root.config(menu=menu)

# Opción de reiniciar
game_menu = tk.Menu(menu, tearoff=0)
game_menu.add_command(label="Iniciar Juego", command=start_game)
menu.add_cascade(label="Juego", menu=game_menu)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

# Controles de movimiento
root.bind("<Up>", lambda e: move_player(0, -1))
root.bind("<Down>", lambda e: move_player(0, 1))
root.bind("<Left>", lambda e: move_player(-1, 0))
root.bind("<Right>", lambda e: move_player(1, 0))

start_game()
root.mainloop()
