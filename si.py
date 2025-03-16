import tkinter as tk
import random
from tkinter import messagebox

WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20

# Posiciones iniciales
player_pos = [1, 1]
obstacles = []
enemies = []
goal = (28, 28)
game_over = False
restart_button = None  # Variable global para el botón de reinicio

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
        
    # Comprobar condiciones de fin después de mover al jugador
    if tuple(player_pos) == goal:
        end_game("¡Has llegado a la meta!", "green")
        return
    elif tuple(player_pos) in enemies:
        end_game("¡Te atrapó un enemigo!", "red")
        return
        
    # Solo actualizar el canvas si el juego continúa
    if not game_over:
        update_enemies_and_canvas()

# Actualizar enemigos y canvas
def update_enemies_and_canvas():
    global enemies, game_over
    
    # Mover enemigos solo si el juego NO ha terminado
    if not game_over:
        new_positions = []
        for i in range(len(enemies)):
            new_pos = enemy_move(enemies[i], tuple(player_pos), obstacles)
            if new_pos not in new_positions:  # Evitar que dos enemigos ocupen la misma posición
                new_positions.append(new_pos)
            else:
                new_positions.append(enemies[i])
        
        enemies = new_positions
        
        # Verificar si un enemigo atrapó al jugador después de moverse
        if tuple(player_pos) in enemies:
            end_game("¡Te atrapó un enemigo!", "red")
            return
    
    update_canvas()

# Actualizar el lienzo
def update_canvas():
    canvas.delete("all")

    # Dibujar obstáculos
    for x, y in obstacles:
        canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill="black")

    # Dibujar enemigos
    for x, y in enemies:
        canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill="red")

    # Dibujar jugador
    x, y = player_pos
    canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill="blue")

    # Dibujar meta
    gx, gy = goal
    canvas.create_rectangle(gx * CELL_SIZE, gy * CELL_SIZE, (gx + 1) * CELL_SIZE, (gy + 1) * CELL_SIZE, fill="green")

# Iniciar el juego
def start_game():
    global player_pos, obstacles, enemies, game_over, restart_button
    
    # Eliminar el botón de reinicio si existe
    if restart_button is not None:
        restart_button.destroy()
        restart_button = None
    
    # Limpiar el canvas
    canvas.delete("all")
    
    # Reiniciar variables del juego
    player_pos = [1, 1]
    
    # Asegurarse de que los obstáculos no bloqueen al jugador o la meta
    obstacles = []
    while len(obstacles) < 40:
        pos = (random.randint(1, 29), random.randint(1, 29))
        if pos != tuple(player_pos) and pos != goal and pos not in obstacles:
            obstacles.append(pos)
            
    # Asegurarse de que los enemigos no empiecen sobre el jugador o la meta
    enemies = []
    while len(enemies) < 3:
        pos = (random.randint(1, 29), random.randint(1, 29))
        if pos != tuple(player_pos) and pos != goal and pos not in obstacles and pos not in enemies:
            enemies.append(pos)
    
    game_over = False
    
    # Volver a habilitar las teclas de movimiento
    root.bind("<Up>", lambda e: move_player(0, -1))
    root.bind("<Down>", lambda e: move_player(0, 1))
    root.bind("<Left>", lambda e: move_player(-1, 0))
    root.bind("<Right>", lambda e: move_player(1, 0))

    update_canvas()

# Terminar el juego
def end_game(message, box_color):
    global game_over, restart_button
    
    # Marcar el juego como terminado
    game_over = True
    
    # Detener el movimiento del jugador
    root.unbind("<Up>")
    root.unbind("<Down>")
    root.unbind("<Left>")
    root.unbind("<Right>")
    
    # Limpiar el canvas y volver a dibujar el estado final
    update_canvas()
    
    # Crear un cuadro de mensaje con fondo de color
    box_width = 500
    box_height = 150
    box_x = WIDTH // 2 - box_width // 2
    box_y = HEIGHT // 2 - box_height // 2
    
    # Dibujar el cuadro con borde
    canvas.create_rectangle(
        box_x, box_y, 
        box_x + box_width, box_y + box_height, 
        fill=box_color, 
        outline="black", 
        width=2
    )
    
    # Mostrar mensaje en el cuadro
    canvas.create_text(
        WIDTH // 2, 
        HEIGHT // 2 - 30, 
        text=message, 
        font=("Arial", 24, "bold"), 
        fill="white"
    )

    # Crear botón para reiniciar en el cuadro
    restart_button = tk.Button(
        root, 
        text="Reiniciar Juego", 
        font=("Arial", 12, "bold"),
        bg="white", 
        command=start_game
    )
    canvas.create_window(WIDTH // 2, HEIGHT // 2 + 30, window=restart_button)

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