import pretty_midi
import flet as ft
import asyncio
from envVar import altura_pantalla, altura_appbar, segundos_en_pantalla, duracion_total_memoria, altura_mapa_memoria, color_inicio_notas, color_final_notas
import pygame
import pygame.midi
import math


colores_originales = {"blanca": ft.colors.WHITE, "negra":ft.colors.BLACK87}

pygame.init()
pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(0)  # 0 es el instrumento de piano en MIDI



global detener
global duracion_total
global altura_del_mapa
global factor_ajuste

detener =  False
teclas_rodeadas = [6,11,13,18,23,25,30,35,37,42,47,49,54,59,61,66,71,73,78,83,85]







class Nota_presionador:
    def __init__(self, nota, duracion, velocidad):
        self.nota = nota
        self.duracion = duracion
        self.velocidad = velocidad

async def play_note_async(nota, velocidad, duracion):
    player.note_on(nota, velocidad)
    await asyncio.sleep(duracion)
    player.note_off(nota, velocidad)

async def presionar_tecla(tecla, nota, duracion, velocidad):
    tecla.bgcolor = ft.colors.BLUE_900
    tecla.update()
    await play_note_async(nota + 21, velocidad, duracion)
    tecla.bgcolor = colores_originales[tecla.data.tipo]
    tecla.update()

async def presionador_teclas(localizaciones, teclas_presionadas_momento):
    await asyncio.gather(*[
        presionar_tecla(localizaciones[nota.nota], nota.nota, nota.duracion, nota.velocidad)
        for nota in teclas_presionadas_momento
    ])

def cargador_auxiliar(momento):
    return [
        Nota_presionador(
            nota.pitch - 21,
            nota.end - nota.start,
            nota.velocity
        )
        for nota in momento
    ]


async def cargador_pantalla(mapa_de_tiempos, claves_mapa_tiempos, localizaciones, page):
    global detener
    notas_por_momento = {}
    for momento, notas in mapa_de_tiempos.items():
        notas_por_momento[momento] = cargador_auxiliar(notas)

    movedor_task = asyncio.create_task(movedor_mapa(page))
    await asyncio.sleep(segundos_en_pantalla)
    tasks = []

    for i, clave in enumerate(claves_mapa_tiempos):
        if detener:
            break
        notas = notas_por_momento[clave]
        task = asyncio.create_task(presionador_teclas(localizaciones, notas))
        tasks.append(task)
        if i + 1 < len(claves_mapa_tiempos):
            await asyncio.sleep(claves_mapa_tiempos[i + 1] - clave)

    # Asegurarse de que todas las tareas de presionar teclas se completen
    await asyncio.gather(*tasks)


        
        


async def movedor_mapa(page):
    global altura_del_mapa, duracion_total, detener
    mapa = page.controls[0].controls[1].controls[1]
    altitud_relativa = page.height - page.height * 0.15 - altura_appbar - altura_pantalla
    distancia_total = altura_del_mapa + altitud_relativa
    print(altura_del_mapa, "Esta es la altura del mapa", distancia_total, "Esta es la distancia total")

    pasos = distancia_total/altitud_relativa
    print(pasos, "Numero de pasos")
    #while pasos > 0 and not detener:
    mapa.bottom -= distancia_total
    mapa.update()




  

#Es la funcion mas compleja, toma todos los eventos del MIDI, los tranforma a un objeto Nota_presionada
#Luego genera un mapa de elementos FLET y lo mapea con elementos de tipo boton para cada nota, este tiene en cuenta la duracion
#total de la pieza para hacer el tamano del mapa y sus posiciones relativas

def generar_mapa(mapa_de_tiempos, claves_mapa_tiempos, page):
    global altura_del_mapa, duracion_total, factor_ajuste
    
    # Calculo de altura relativa
    altura_relativa = page.height - page.height * 0.15 - altura_appbar - altura_pantalla

    # Obtención de la última nota y su duración
    ultimo_momento = mapa_de_tiempos[claves_mapa_tiempos[-1]]
    notas_ultimo_momento = cargador_auxiliar(ultimo_momento)
    duracion_nota_mas_larga = max(notas_ultimo_momento, key=lambda nota: nota.duracion).duracion

    # Calculo de la duración total
    duracion_total = duracion_nota_mas_larga + claves_mapa_tiempos[-1]


    duracion_total_memoria = duracion_total * 1000

    
    # Duración total de la animación
    duracion_total_animacion = duracion_total + segundos_en_pantalla

    print(duracion_total_animacion*1000, math.floor(duracion_total_animacion * 1000), "Se perdieron",duracion_total_animacion*1000-math.floor(duracion_total_animacion * 1000), "segundos" )

    # Calculo de la altura del mapa ajustada
    altura_del_mapa = duracion_total / segundos_en_pantalla * altura_relativa
    print(altura_del_mapa, "Esta es la altura del mapa")
    # Creación del mapa visual
    mapa = ft.Stack(
        controls=[
            ft.Container(
                width=page.width,
                height=page.height,
                image_src="fondo.jpg",
                image_fit=ft.ImageFit.COVER,
                image_repeat=ft.ImageRepeat.NO_REPEAT
            ),
            ft.Container(
                content=ft.Stack(
                    controls=[],
                    height=altura_del_mapa,
                    width=page.width
                ),
                width=page.width,
                height=altura_del_mapa,
                bottom=altura_relativa,
                bgcolor=ft.colors.TRANSPARENT,
                left=0,
                animate_position=ft.animation.Animation(int(math.floor(duracion_total_animacion * 1000)), ft.AnimationCurve.LINEAR)
            )
        ],
        width=page.width,
        height=altura_relativa,
        data="mapa"
    )
    
    mapa_notas = mapa.controls[1].content.controls
    matrix_posiciones = page.controls[0].controls[0].controls


    # Posicionamiento y añadido de notas
    for i, clave in enumerate(claves_mapa_tiempos):
        momento = mapa_de_tiempos[clave]
        teclas_presionadas_momento = cargador_auxiliar(momento)

        for tecla in teclas_presionadas_momento:
            # Cálculo de ancho y posición X
            for posicion in matrix_posiciones:
                if posicion.data.marca == tecla.nota:
                    posicion_x = posicion.left
                    ancho = posicion.width
                    break

            # Cálculo de proporciones
            proporcion_nota = tecla.duracion / duracion_total
            proporcion_espaciado_y = clave / duracion_total

            # Creación de la nota visual
            nota = ft.Container(
                width=ancho,
                height=proporcion_nota * altura_del_mapa,
                left=posicion_x,
                bottom=proporcion_espaciado_y * altura_del_mapa,
                bgcolor=ft.colors.GREEN_ACCENT_700,
                data=tecla.nota,
                border_radius=ft.border_radius.all(1),
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[color_inicio_notas, color_final_notas],
                ),
                padding=ft.padding.only(bottom=3)
            )
            mapa_notas.append(nota)

    # Actualización de la página
    page.controls[0].controls[1] = mapa
    page.update()






#FUncion auxiliar que mapea y luego ejecuta las notas
async def mapeador(pista_midi,localizaciones, page,iniciar):
    global factor_ajuste
    # Crear un diccionario que contendrá todos los eventos del MIDI y una lista que tendrá las claves de dichos eventos
    mapa_de_tiempos = {}
    #Arreglo que contiene todos los tiempos de manera cronologica
    claves_mapa_tiempos = []

    #Recorre las notas buscando sus inicios, si ese momento no esta ya registrado en las variables anteriores, las agrega 
    for nota in pista_midi.notes:
        momento_inicio = nota.start

        if momento_inicio not in mapa_de_tiempos:
            mapa_de_tiempos[momento_inicio] = []
            claves_mapa_tiempos.append(momento_inicio)
        mapa_de_tiempos[momento_inicio].append(nota)

    primer_tiempo = 0
    if claves_mapa_tiempos[0] != 0:
        for clave in sorted(claves_mapa_tiempos):
            if clave != 0:
                print("Se ajusto la pieza en un factor de", clave)
                primer_tiempo = clave
                factor_ajuste = clave
                break

    claves_mapa_tiempos = [clave - primer_tiempo for clave in claves_mapa_tiempos]

    # Ajustar mapa_de_tiempos
    mapa_de_tiempos = {clave - primer_tiempo: valor for clave, valor in mapa_de_tiempos.items()}


    if iniciar:
        generar_mapa(mapa_de_tiempos, sorted(claves_mapa_tiempos),page)
    else:
        await cargador_pantalla(mapa_de_tiempos, sorted(claves_mapa_tiempos),localizaciones, page)


#define un midi
def definir_midi(page, url="ballade1.mid"):
    page.appbar.title = ft.Text(f"{url}")
    page.update()
    midi_data = pretty_midi.PrettyMIDI(url)
    pista_midi = midi_data.instruments[0]
    return pista_midi

async def iniciar(pista_midi, localizaciones, page, iniciar):
    await mapeador(pista_midi, localizaciones, page, iniciar)

def detener_todo():
    global detener
    detener = True