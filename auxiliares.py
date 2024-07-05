import flet as ft
from envVar import altura_pantalla, altura_appbar, color_appbar
import manejadorMidi

def resize(page):
    contador = 0
    piano = page.controls[0].controls[2]
    mapa = page.controls[0].controls[1]
    pantalla = page.controls[0].controls[0]


    piano.width = page.width
    piano.height = page.height * 0.15
    for fila_teclas in piano.controls:
        fila_teclas.height = (page.height * 0.15) / 1.5
        fila_teclas.width = (page.width * 0.15) / 1.5
        fila_teclas.left = 0

        if contador == 0:
            fila_teclas.bottom = 0
            fila_teclas.height = page.height * 0.15
            contador += 1
        else:
            fila_teclas.bottom = 0+page.height * 0.15 - fila_teclas.height 

        for tecla in fila_teclas.content.controls:
            if tecla.data.tipo == "blanca":
                tecla.width = page.width/52
                tecla.height = page.height * 0.15
                tecla.data.ancho = page.width/52
                tecla.data.altura = page.height * 0.15
            else:
                tecla.width =  (page.width/52)*0.5
                tecla.height =  page.height * 0.15  / 1.5
                tecla.data.ancho =  (page.width/52)*0.5
                tecla.data.altura =  page.height * 0.15  / 1.5  
                if tecla.data.marca == 2:
                    tecla.margin = ft.margin.only(left=((page.width/52)-(tecla.data.ancho/2)))
                elif tecla.data.marca in [5,10,17,22,29,34,41,46,53,58,65,70,77,82]:
                    tecla.margin = ft.margin.only(left=((page.width/52)*2-(tecla.data.ancho)))
                else:
                    tecla.margin=ft.margin.only(left=(page.width/52-tecla.data.ancho))
    
    pantalla.width = page.width
    pantalla.height = altura_pantalla

    ancho_rellenado = 0

    ancho_teclas_blancas = page.width/52
    ancho_teclas_negras = ancho_teclas_blancas * 0.5
    mapa.height = page.height - page.height*0.15 - altura_pantalla - altura_appbar
    mapa.width = page.width
    mapa.controls[1].width = page.width
    #PARA EL FONDO DE PANTALLA
    mapa.controls[0].width = page.width
    mapa.controls[0].height = page.height - page.height*0.15 - altura_pantalla - altura_appbar


    for i, tecla in enumerate(pantalla.controls[:88]):
        if tecla.data.tipo == "blanca":
            siguiente_es_negra = (i + 1 < len(pantalla.controls[:88])) and pantalla.controls[i + 1].data.tipo == "negra"
            anterior_es_negra = (i - 1 >= 0) and pantalla.controls[i - 1].data.tipo == "negra"

            if i == 0:
                ancho_teclas_blancas -= ancho_teclas_negras / 2
            elif siguiente_es_negra and anterior_es_negra:
                ancho_teclas_blancas -= ancho_teclas_negras
            elif siguiente_es_negra or anterior_es_negra:
                ancho_teclas_blancas -= ancho_teclas_negras / 2
            elif i == len(pantalla.controls[:88]) - 1:
                ancho_teclas_blancas = page.width / 52

            tecla.width = ancho_teclas_blancas
            tecla.height = altura_pantalla
            tecla.data.ancho = ancho_teclas_blancas
            tecla.data.altura = altura_pantalla
            tecla.left = ancho_rellenado

            ancho_rellenado += ancho_teclas_blancas
            ancho_teclas_blancas = page.width / 52

        else:
            tecla.width =  ancho_teclas_negras
            tecla.height =altura_pantalla
            tecla.data.ancho =  ancho_teclas_negras
            tecla.data.altura = altura_pantalla
            tecla.left = ancho_rellenado   

            ancho_rellenado += ancho_teclas_negras        

        mapa_notas = mapa.controls[1].content.controls 
        matrix_posiciones = page.controls[0].controls[0].controls
        for nota in mapa_notas:
            ancho = 0
            posicion_x = 0
            for i in range(0,88):
                if matrix_posiciones[i].data.marca == nota.data:
                    
                    posicion_x = matrix_posiciones[i].left
                    ancho =  matrix_posiciones[i].width
                    break
            nota.width = ancho
            nota.left = posicion_x

    page.update()



def agregar_appbar(page):
    page.appbar= ft.AppBar(
        toolbar_height=altura_appbar,
        is_secondary=True,
        title=ft.Text("No se ha definido la pista de audio."),
        center_title=False,
        bgcolor=color_appbar,
        actions=[
            ft.IconButton(icon=ft.icons.PLAY_ARROW),
            ft.IconButton(ft.icons.STOP_CIRCLE),
            ft.IconButton(ft.icons.UPLOAD_FILE),
        ],
    )

    page.update()


