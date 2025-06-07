# cliente_gui.py
import socket
import threading
import tkinter as tk


SERVER_IP = "192.168.114.178"  # Cambia esto con la IP de la Pico W
PORT = 1717

def bot1():
    patron.append(0)
    if len(patron) == 7:
        regresar()

def bot2():
    patron.append(1)
    if len(patron) == 7:
        regresar()

def bot3():
    patron.append(2)
    if len(patron) == 7:
        regresar()

def bot4():
    patron.append(3)
    if len(patron) == 7:
        regresar()

def regresar():
    global window, patron
    window.destroy()
    send_message()
    ventana()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():
    global status_label
    try:
        client_socket.connect((SERVER_IP, PORT))
        threading.Thread(target=receive_messages, daemon=True).start()
        status_label.config(text="Conectado al servidor")
    except Exception as e:
        status_label.config(text=f"Error: {e}")

def send_message():
    global window, patron
    msg = patron
    if msg:
        client_socket.send(msg.encode())
        window.delete(0, tk.END)

def receive_messages():
    global text_area
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            text_area.insert(tk.END, f"Raspberry: {msg}\n")
        except:
            break

def salir():
    try:
        client_socket.close()
    except:
        pass
    window.destroy()

def modo_adicional():
    global window, patron

    window.destroy()
    window = tk.Tk()
    window.minsize(width=400, height=400)

    send_message()

    boton1 = tk.Button(text='   ', fg='white', bg='green', width = 12, height = 5, command=bot1)
    boton1.place(x=100, y=100)

    boton2 = tk.Button(text='   ', fg='white', bg='red', width = 12, height = 5, command=bot2)
    boton2.place(x=200, y=100)

    boton3 = tk.Button(text='   ', fg='white', bg='black', width = 12, height = 5, command=bot3)
    boton3.place(x=100, y=200)

    boton4 = tk.Button(text='   ', fg='white', bg='blue', width = 12, height = 5, command=bot4)
    boton4.place(x=200, y=200)

def ventana():
    global window, patron, status_label, text_area

    patron = []

    window = tk.Tk()
    window.minsize(width=500, height=500)

    texto = tk.Label(text='Presione sí')
    texto.place(x=220, y=100)

    status_label = tk.Label(text='Desconectado')
    status_label.pack()

    text_area = tk.Label(height=10, width=60)

    boton_modo_adicional = tk.Button(text='Modo adicional >:)', fg='white', bg='red', width=15, command=modo_adicional)
    boton_modo_adicional.place(x=190, y=250)

    connect()

    window.mainloop()

ventana()
