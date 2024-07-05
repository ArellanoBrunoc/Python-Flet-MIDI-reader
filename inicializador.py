import flet as ft
from envVar import altura_pantalla

class Nota:
    def __init__(self, tipo: str, estado: bool, ancho: float, altura: float, marca: int):
        """
        Inicializa una nueva nota para el constructor del piano.

        :param tipo: str, puede ser 'blanca' o 'negra'
        :param estado: bool, el estado de la nota (presionada o no presionada)
        :param ancho: float, el ancho de la nota en pixeles
        :param altura: float, el alto de la nota en pixeles
        :param marca: int, la marca de la nota desde el A0 (1) hasta el C8 (88)
        """
        if tipo not in ['blanca', 'negra']:
            raise ValueError("El tipo de nota debe ser 'blanca' o 'negra'")
        if not isinstance(marca, int) or not (1 <= marca <= 88):
            raise ValueError("La marca debe ser un número entero entre 1 y 88")
        if not isinstance(altura, (int, float)) or altura <= 0:
            raise ValueError("La altura debe ser un número positivo")
        if not isinstance(ancho, (int, float)) or ancho <= 0:
            raise ValueError("El ancho debe ser un número positivo")


        self.tipo = tipo
        self.estado = estado
        self.ancho =  ancho
        self.altura = altura
        self.marca = marca

    def __repr__(self):
        return f"Nota(tipo='{self.tipo}', estado={self.estado}, ancho={self.ancho}, altura={self.altura})"
    
    def alternar(self):
        """Alterna el estado de la nota entre 0 y 1."""
        self.estado = 1 - self.estado



def inicializar(width, height):
    notas, ancho_teclas_blancas = inicializar_notas(width, height)
    piano, localizador_piano = creador_piano(width, height, notas,ancho_teclas_blancas)
    pantalla, localizador_pantalla = creador_pantalla(width, height, notas, ancho_teclas_blancas)
    return piano, localizador_piano, pantalla, localizador_pantalla

def inicializar_notas(width, height):
    ancho_teclas_blancas = width/52
    ancho_teclas_negras = ancho_teclas_blancas * 0.5

    alto_teclas_negras = height*0.15 / (1.5)
    alto_teclas_blancas = alto_teclas_negras * 1.5

    notas_en_orden = []
    for i in range(1, 4):
        if i == 2:
            nota = Nota("negra", False, ancho_teclas_negras, alto_teclas_negras, i)
        else:
            nota = Nota("blanca", False, ancho_teclas_blancas, alto_teclas_blancas, i)
        notas_en_orden.append(nota)

    # Notas del resto del rango (4-88)

    for i in range(0, 85):

        if i % 12 in [1, 3, 6, 8, 10]: 
            nota = Nota("negra", False, ancho_teclas_negras, alto_teclas_negras, i+4)
            
        else:
            nota = Nota("blanca", False, ancho_teclas_blancas, alto_teclas_blancas, i+4)

        notas_en_orden.append(nota)
    return notas_en_orden, ancho_teclas_blancas

def creador_piano(width, height, notas, ancho_teclas_blancas):
    colors = {"blanca": ft.colors.WHITE, "negra": ft.colors.BLACK87}
    piano_container = ft.Stack(
                                controls=[], 
                                width=width, 
                                height=(height * 0.15),
                                
                                )
    negras = ft.Container(
                        content=ft.Row([], spacing=0), 
                        width=width, 
                        height=(height * 0.15) / 1.5,
                        bottom=0+height*0.15 - height*0.15 / (1.5)
                        )
    blancas = ft.Container(
                        content=ft.Row([], 
                                       spacing=0), 
                        width=width, 
                        height=(height * 0.15),
                        bottom=0
                        )

    localizador = {}
    for nota in notas:
        if nota.tipo == "negra":
            # Encuentra el margen de la tecla negra
            if (nota.marca) == 2 :
                negra = ft.Container(

                        bgcolor=colors[nota.tipo],
                        height=nota.altura,
                        width=nota.ancho,
                        data=nota,
                        margin=ft.margin.only(left=(ancho_teclas_blancas-nota.ancho/2)),
                        border=ft.border.all(0.1, ft.colors.BLACK12),
                        border_radius=ft.border_radius.only(bottom_left=4, bottom_right=4),



                    )

                negras.content.controls.append(negra)
                localizador[nota.marca] = negra

            elif nota.marca in [5,10,17,22,29,34,41,46,53,58,65,70,77,82]:
                negra = ft.Container(
                        bgcolor=colors[nota.tipo],
                        height=nota.altura,
                        width=nota.ancho,
                        data=nota,
                        margin=ft.margin.only(left=(ancho_teclas_blancas*2-(nota.ancho))),
                        border=ft.border.all(0.1, ft.colors.BLACK12),
                        border_radius=ft.border_radius.only(bottom_left=4, bottom_right=4) , 
            
                    )
                negras.content.controls.append(negra)
                localizador[nota.marca] = negra

            else:
                negra = ft.Container(
                        bgcolor=colors[nota.tipo],
                        height=nota.altura,
                        width=nota.ancho,
                        data=nota,
                        margin=ft.margin.only(left=(ancho_teclas_blancas-nota.ancho)),
                        border=ft.border.all(0.1, ft.colors.BLACK12),
                        border_radius=ft.border_radius.only(bottom_left=4, bottom_right=4)  ,
    
                          
                    )
                negras.content.controls.append(negra)
                localizador[nota.marca] = negra
        else:
            blanca =ft.Container(
                    
                    bgcolor=colors[nota.tipo],
                    height=nota.altura,
                    width=nota.ancho,
                    data=nota,
                    margin=0,
                    padding=0,
                    border=ft.border.all(1, ft.colors.BLACK12),
                    border_radius=ft.border_radius.only(bottom_left=2, bottom_right=2)    ,
  
                ) 
            blancas.content.controls.append(blanca)
            localizador[nota.marca] = blanca


    piano_container.controls.append(blancas)
    piano_container.controls.append(negras)
    return piano_container, localizador






def creador_pantalla(width, height, notas, ancho_teclas_blancas):
    colors = {"blanca": ft.colors.WHITE, "negra": ft.colors.BLACK87}
    altura_relativa = altura_pantalla

    ancho_teclas_blancas = width/52
    ancho_teclas_negras = ancho_teclas_blancas * 0.5


    pantalla_container = ft.Stack(
                                controls=[], 
                                width=width, 
                                height=10,
                                
                                )
    # Variables para gestionar el posicionamiento de teclas negras
    ancho_rellenado = 0
    localizador = {}
    for nota in notas:
        nota.altura = altura_relativa

        if nota.tipo == "negra":
            nota.ancho = ancho_teclas_negras
            # Encuentra el margen de la tecla negra
            negra = ft.Container(
                        bgcolor=ft.colors.BLUE_800,
                        height=altura_relativa,
                        width=ancho_teclas_negras,
                        data=nota,
                        left= ancho_rellenado,
                        margin = 0,
                        border=ft.border.all(0.1, ft.colors.BLACK12),
                        #border_radius=ft.border_radius.only(bottom_left=4, bottom_right=4),
                    )
            ancho_rellenado += ancho_teclas_negras
            pantalla_container.controls.append(negra)
            localizador[nota.marca] = negra

        else:
            nota.ancho = ancho_teclas_blancas
            blanca =ft.Container(
                    
                    bgcolor=ft.colors.DEEP_ORANGE_900,
                    height=altura_relativa,
                    width=ancho_teclas_blancas,
                    data=nota,
                    left= ancho_rellenado,
                    margin=0,
                    padding=0,
                    border=ft.border.all(1, ft.colors.BLACK12),
                    #border_radius=ft.border_radius.only(bottom_left=2, bottom_right=2)    ,
  
                ) 
            
            ancho_rellenado += ancho_teclas_blancas
            pantalla_container.controls.append(blanca)
            localizador[nota.marca] = blanca

    return pantalla_container, localizador






def inicializar_pantalla(width, height):

    pantalla =  ft.Stack(
                        controls=[],
                         width=width,
                         height=40
                         )
    pantalla.controls.append(ft.Container(
                                        bgcolor=ft.colors.BLACK45,
                                        top = 0 ,
                                        left=0,
                                        width=width,
                                        height=40
                                        
                                        )
                            )

    return pantalla