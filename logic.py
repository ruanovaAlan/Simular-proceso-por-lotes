import time
import random

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
def generar_lotes(n):
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


def mostrar_lotes(lotes):
    skip

def update_clock(relojGlobal_label, root): #Función que actualiza el reloj
    global start_time
    if start_time is None:
        start_time = time.time()
    elapsed_time = time.time() - start_time
    relojGlobal_label.config(text=f"Reloj: {int(elapsed_time)} segundos")
    root.after(1000, update_clock, relojGlobal_label, root)  # Actualiza el reloj cada 1000 milisegundos
    

generar_lotes(3)
lotes_a_txt()