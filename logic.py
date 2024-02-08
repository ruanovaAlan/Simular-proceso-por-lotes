import time
import random

start_time = None

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
    lotes = []
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
    
    return lotes

#Funcion para escribir lotes a un archivo
def escribir_lotes_a_archivo(n):
    lotes = generar_lotes(n)

    with open('datos.txt', 'w') as f:
        for i, lote in enumerate(lotes, start=1):
            f.write(f'Lote {i}:\n')
            f.write('\n')
            for proceso in lote:
                f.write(f"{proceso['numero_programa']}. {proceso['nombre']}\n")
                f.write(f"{proceso['operacion']}\n")
                f.write(f"TME: {proceso['tiempo_maximo']}\n")
                f.write('\n')
                f.write('\n')
            f.write('\n')

escribir_lotes_a_archivo(8)


def update_clock(relojGlobal_label, root): #Función que actualiza el reloj
    global start_time
    if start_time is None:
        start_time = time.time()
    elapsed_time = time.time() - start_time
    relojGlobal_label.config(text=f"Reloj: {int(elapsed_time)} segundos")
    root.after(1000, update_clock, relojGlobal_label, root)  # Actualiza el reloj cada 1000 milisegundos
    

