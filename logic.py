import time
import random
from tkinter import *
from tkinter import ttk

start_time = None
lotes = []

#Funcion que retorna un numero aleatorio para el tiempo maximo estimado de un proceso
def getTiempoMaxEstimado():
    return random.randint(6, 12)

#Funcion para generar una operacion aleatoria
def getOperacion():
    operadores = ['+','-','*','/']
    operador = random.choice(operadores)
    datos = (random.randint(0,10), random.randint(0,10))
    while operador == '/' and datos[1] == 0:
        datos = (random.randint(0,10), random.randint(0,10))    
    operacion = f"{str(datos[0])} {operador} {str(datos[1])}"
    return operacion



#Funcion para generar lotes de procesos con datos aleatorios
def crear_lotes(n):
    nombre_programadores = ['Alan', 'Juan', 'Jenny', 'Luis', 'Maria', 'Pedro', 'Sofia', 'Tom', 'Valeria', 'Ximena']
    num_programa = 1
    global lotes
    lote = []
    
    for i in range(n):
        proceso = {
            'nombre': random.choice(nombre_programadores),
            'operacion': getOperacion(),
            'tiempo_maximo': getTiempoMaxEstimado(),
            'numero_programa': num_programa,
            'estado': 0 # 0 = en espera, 1 = en ejecucion, 2 = terminado   
        }
        
        lote.append(proceso)
        num_programa += 1
        
        if len(lote) == 5:
            lotes.append(lote)
            lote = []
    
    if lote:
        lotes.append(lote)
    
    # return lotes



#Funcion para escribir lotes a un archivo
def lotes_a_txt():
    global lotes
    if lotes != []:
        with open('datos.txt', 'w') as file:
            for i, lote in enumerate(lotes, start=1):
                file.write(f'Lote {i}:\n')
                file.write('\n')
                for proceso in lote:
                    file.write(f"{proceso['numero_programa']}. {proceso['nombre']}\n")
                    file.write(f"{proceso['operacion']}\n")
                    file.write(f"TME: {proceso['tiempo_maximo']}\n")
                    file.write('\n')
                    file.write('\n')
                file.write('\n')


def resultados_a_txt():
    global lotes
    if lotes != []:
        with open('Resultados.txt', 'w') as file:
            for i, lote in enumerate(lotes, start=1):
                file.write(f'Lote {i}:\n')
                file.write('\n')
                for proceso in lote:
                    resultado = eval(proceso['operacion'])
                    
                    file.write(f"{proceso['numero_programa']}. {proceso['nombre']}\n")
                    file.write(f"{proceso['operacion']} = {resultado}\n")
                    file.write(f"TME: {proceso['tiempo_maximo']}\n")
                    file.write('\n')
                    file.write('\n')
                file.write('\n')

def check_procesos_ejecucion():
    global lotes
    for lote in lotes:
        for proceso in lote:
            if proceso['estado'] == 1:
                return True
    return False

def contar_procesos_en_espera(lote):
    count = 0
    for proceso in lote:
        if proceso['estado'] == 0:
            count += 1
    return count


def ejecutar_proceso(lotes, noLotesPendientes_label, ejecucion_text, root, procesosEnEspera_text,tiempo_inicio_proceso=None):
    if lotes:  # Si hay lotes pendientes
        lote_actual = lotes[0]  # Toma el primer lote
        procesoEnEjecucion = lote_actual[0]  # Toma el primer proceso en espera
        if tiempo_inicio_proceso is None:  # Si es la primera vez que se llama a la función para este proceso
            tiempo_inicio_proceso = time.time() - start_time
        tiempo_transcurrido = time.time() - start_time - tiempo_inicio_proceso
        tiempo_restante = procesoEnEjecucion['tiempo_maximo'] - tiempo_transcurrido
        if tiempo_restante <= 0:  # Si el tiempo restante ha llegado a cero
            lote_actual.pop(0)  # Elimina el proceso de la lista de procesos en espera
            tiempo_inicio_proceso = None  # Resetea el tiempo de inicio para el próximo proceso
            if not lote_actual:  # Si el lote actual está vacío
                lotes.pop(0)  # Elimina el lote de la lista de lotes

        # Actualiza la interfaz de usuario
        ejecucion_text.delete('1.0', END)  # Limpia el widget Text antes de insertar nuevo texto
        ejecucion_text.insert(END, f"{procesoEnEjecucion['numero_programa']}. {procesoEnEjecucion['nombre']}\n{procesoEnEjecucion['operacion']}\nTME: {round(tiempo_restante) if tiempo_restante > 0 else 0}")
        cantidad_lotes = max(0, len(lotes) - 1)
        noLotesPendientes_label.config(text=f"# De lotes pendientes: {cantidad_lotes}")
        procesosEnEspera_text.delete('1.0', END)  # Limpia el widget Text antes de insertar nuevo texto
        # for proceso in lote_actual[1:]:  # Para cada proceso en espera en el lote actual
        #     procesosEnEspera_text.insert(END, f"{proceso['numero_programa']}. {proceso['nombre']}\n{proceso['operacion']}\nTME: {proceso['tiempo_maximo']}\n\n")
        # root.after(1000, ejecutar_proceso, lotes, noLotesPendientes_label, ejecucion_text, root, procesosEnEspera_text,tiempo_inicio_proceso)
        if len(lote_actual) == 1:  # Si solo queda un proceso en el lote actual
            if lotes[1:]:  # Si hay más lotes
                lote_siguiente = lotes.pop(1)  # Toma el siguiente lote
                lote_actual.extend(lote_siguiente)  # Añade los procesos del siguiente lote a la lista de procesos en espera

        for proceso in lote_actual[1:]:  # Para cada proceso en espera en el lote actual
            procesosEnEspera_text.insert(END, f"{proceso['numero_programa']}. {proceso['nombre']}\n{proceso['operacion']}\nTME: {proceso['tiempo_maximo']}\n\n")
        root.after(1000, ejecutar_proceso, lotes, noLotesPendientes_label, ejecucion_text, root, procesosEnEspera_text, tiempo_inicio_proceso)

def generar_procesos(noProcesos_entry, ejecucion_text, noLotesPendientes_label, root, procesosEnEspera_text):
    global lotes
    n = int(noProcesos_entry.get())
    crear_lotes(n)
    lotes_a_txt()

    ejecutar_proceso(lotes, noLotesPendientes_label, ejecucion_text, root, procesosEnEspera_text)  # Inicia el "bucle"





#Función que actualiza el reloj
def update_clock(relojGlobal_label, root): 
    global start_time
    if start_time is None:
        start_time = time.time()
    elapsed_time = time.time() - start_time
    relojGlobal_label.config(text=f"Reloj: {int(elapsed_time)} segundos")
    root.after(1000, update_clock, relojGlobal_label, root)  # Actualiza el reloj cada 1000 milisegundos
    

