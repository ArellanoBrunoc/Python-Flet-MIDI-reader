import flet as ft
from inicializador import inicializar
import time
import manejadorMidi, auxiliares
import asyncio
from concurrent.futures import ThreadPoolExecutor
from envVar import  altura_appbar, altura_pantalla, color_appbar, color_progressbar

colores_originales = {"blanca": ft.colors.WHITE, "negra": ft.colors.BLACK87}

executor = ThreadPoolExecutor(max_workers=60)


def main(page: ft.Page):
    pista_midi = ""
    inicio_predeterminado = ft.Stack(controls=[ft.Container(image_src="fondo.jpg", image_fit=ft.ImageFit.COVER, image_repeat=ft.ImageRepeat.NO_REPEAT,width=page.width, height=page.height-page.height*0.15-altura_appbar - altura_pantalla),ft.Container(content=ft.Stack(controls=[]))])
 

    def pick_files_result(e: ft.FilePickerResultEvent):
        nonlocal pista_midi
        if e.files != None:
            pista_midi = manejadorMidi.definir_midi(page, e.files[0].path)
        

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)


    page.overlay.append(pick_files_dialog)
    def on_resize(e):
        auxiliares.resize(page)

    
    def run_coroutine(coroutine_func, *args):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(coroutine_func(*args))
        loop.close()

    def comenzar(e):
        nonlocal pista_midi
        if pista_midi == "":
            return
        manejadorMidi.detener = False
        page.appbar.actions[0].disabled = True
        page.update()
        # Ejecutar las coroutines en threads separados
        executor.submit(run_coroutine, manejadorMidi.iniciar, pista_midi, localizaciones, page, True)
        time.sleep(4)
        executor.submit(run_coroutine, manejadorMidi.iniciar, pista_midi, localizaciones, page, False)

    def parar_ejecucion(e):
        manejadorMidi.detener_todo()
        auxiliares.resize(page)
        page.controls[0].controls[1] = inicio_predeterminado
        page.update()
        time.sleep(5)
        page.appbar.actions[0].disabled = False
        page.update()
    # se define la bs para mensajes al usuario:

    page.on_resize = on_resize
    page.window.resizable = True
    page.padding = ft.padding.all(0)
    page.scroll = ft.ScrollMode.HIDDEN
    page.theme_mode = ft.ThemeMode.DARK


    piano, localizaciones, pantalla, localizaciones_pantalla = inicializar(page.width, page.height)

    columna_display= ft.Column(controls=[], spacing=0)
    page.add(columna_display)
    #ProgressBar = ft.ProgressRing()
    #page.overlay.append(ProgressBar)
    #page.update()
    auxiliares.agregar_appbar(page)


    page.appbar.actions[0].on_click = comenzar
    page.appbar.actions[1].on_click = parar_ejecucion
    page.appbar.actions[2].on_click = lambda _: pick_files_dialog.pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.CUSTOM, allowed_extensions=["mid"], dialog_title="Abrir MIDI")




    columna_display.controls.append(pantalla)
    columna_display.controls.append(inicio_predeterminado)
    columna_display.controls.append(piano)


    page.update()

    auxiliares.resize(page)


    #page.controls[0].controls[1].controls[0].bottom = -60

    page.update()





ft.app(target=main)
