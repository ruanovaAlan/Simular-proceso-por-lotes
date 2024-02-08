import time

start_time = None

def update_clock(relojGlobal_label, root): #Función que actualiza el reloj
    global start_time
    if start_time is None:
        start_time = time.time()
    elapsed_time = time.time() - start_time
    relojGlobal_label.config(text=f"Reloj: {int(elapsed_time)} segundos")
    root.after(1000, update_clock, relojGlobal_label, root)  # Actualiza el reloj cada 1000 milisegundos