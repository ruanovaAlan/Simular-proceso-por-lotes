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

# def generar_procesos(noProcesos_entry, ejecucion_text, noLotesPendientes_label):
#     n = int(noProcesos_entry.get())
#     tiempo_actual = 0
#     global lotes
#     crear_lotes(n)
#     lotes_a_txt()

#     cantidad_lotes = len(lotes)
#     for lote in lotes:
#         cantidad_lotes -= 1
#         noLotesPendientes_label.config(text=f"# De lotes pendientes: {cantidad_lotes}")
#         for proceso in lote:
#             tiempo_inicio = time.time()
#             while True:
#                 tiempo_actual = time.time()
#                 tiempo_transcurrido = tiempo_actual - tiempo_inicio
#                 tiempo_restante = proceso['tiempo_maximo'] - tiempo_transcurrido
#                 if tiempo_restante <= 0:
#                     break
#                 ejecucion_text.delete('1.0', END)  # Limpia el widget Text antes de insertar nuevo texto
#                 ejecucion_text.insert(END, f"{proceso['numero_programa']}. {proceso['nombre']}\n{proceso['operacion']}\nTME: {round(tiempo_restante)}")
#                 time.sleep(1)


# def generar_procesos(noProcesos_entry, ejecucion_text, noLotesPendientes_label):
#     n = int(noProcesos_entry.get())
#     global lotes
#     crear_lotes(n)
#     lotes_a_txt()
#     procesosEnEspera = []
#     procesoEjecutandose = []

#     cantidad_lotes = len(lotes)
#     for lote in lotes:
#         procesosEnEspera.append(lote)
#         cantidad_lotes -= 1
#         noLotesPendientes_label.config(text=f"# De lotes pendientes: {cantidad_lotes}")
#         for proceso in lote:
#             tiempo_restante = proceso['tiempo_maximo']

#             # Función interna para actualizar el widget de texto y simular la ejecución del proceso
#             def actualizar_ejecucion():
#                 nonlocal tiempo_restante
#                 if tiempo_restante > 0:
#                     tiempo_restante -= 1
#                     ejecucion_text.delete('1.0', END)
#                     ejecucion_text.insert(END, f"{proceso['numero_programa']}. {proceso['nombre']}\n{proceso['operacion']}\nTME: {round(tiempo_restante)}")
#                     ejecucion_text.after(1000, actualizar_ejecucion)  # Programa la próxima actualización después de 1 segundo

#             # Llama a la función interna para iniciar la actualización
#             actualizar_ejecucion()


def ejecutar_proceso(procesosEnEspera, noLotesPendientes_label, cantidad_lotes, ejecucion_text, root, tiempo_inicio_proceso=None):
    global start_time
    if procesosEnEspera:  # Si hay procesos en espera
        procesoEnEjecucion = procesosEnEspera[0]  # Toma el primer proceso en espera
        if tiempo_inicio_proceso is None:  # Si es la primera vez que se llama a la función para este proceso
            tiempo_inicio_proceso = time.time() - start_time
        tiempo_transcurrido = time.time() - start_time - tiempo_inicio_proceso
        tiempo_restante = procesoEnEjecucion['tiempo_maximo'] - tiempo_transcurrido
        if tiempo_restante <= 0:  # Si el tiempo restante ha llegado a cero
            procesosEnEspera.pop(0)  # Elimina el proceso de la lista de procesos en espera
            tiempo_inicio_proceso = None  # Resetea el tiempo de inicio para el próximo proceso

        # Actualiza la interfaz de usuario
        ejecucion_text.delete('1.0', END)  # Limpia el widget Text antes de insertar nuevo texto
        ejecucion_text.insert(END, f"{procesoEnEjecucion['numero_programa']}. {procesoEnEjecucion['nombre']}\n{procesoEnEjecucion['operacion']}\nTME: {round(tiempo_restante) if tiempo_restante > 0 else 0}")
        
        root.after(1000, ejecutar_proceso, procesosEnEspera, noLotesPendientes_label, cantidad_lotes, ejecucion_text, root, tiempo_inicio_proceso)  # Programa la próxima iteración del "bucle"


def generar_procesos(noProcesos_entry, ejecucion_text, noLotesPendientes_label, root):
    global lotes
    n = int(noProcesos_entry.get())
    crear_lotes(n)
    lotes_a_txt()

    cantidad_lotes = len(lotes)
    for lote in lotes:
        procesosEnEspera = lote[:]
        cantidad_lotes -= 1
        noLotesPendientes_label.config(text=f"# De lotes pendientes: {cantidad_lotes}")
        ejecutar_proceso(procesosEnEspera, noLotesPendientes_label, cantidad_lotes, ejecucion_text, root)  # Inicia el "bucle"
        # lotes.remove(lote)






#Función que actualiza el reloj
def update_clock(relojGlobal_label, root): 
    global start_time
    if start_time is None:
        start_time = time.time()
    elapsed_time = time.time() - start_time
    relojGlobal_label.config(text=f"Reloj: {int(elapsed_time)} segundos")
    root.after(1000, update_clock, relojGlobal_label, root)  # Actualiza el reloj cada 1000 milisegundos
    

