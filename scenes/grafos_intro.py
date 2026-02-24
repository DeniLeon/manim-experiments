from manim import *

class IntroGrafos(Scene):
    def construct(self):
        titulo = Text("Grafos", font_size=64)
        subtitulo = Text("Nodos y aristas (prueba.1 a ver si funciona :c )",font_size = 36).next_to(titulo, DOWN)

        self.play(Write(titulo))
        self.play(FadeIn(subtitulo, shift=UP))
        self.wait(0.8)

        self.play(VGroup(titulo,subtitulo).animate.to_edge(UP))
        self.wait(0.2)


        #un nodo simple, un ciculo con etiqueta

        nodo_a= Circle(radius= 0.45)
        etiqueta_a = Text("A", font_size=36).move_to(nodo_a.get_center())
        grupo_a = VGroup(nodo_a, etiqueta_a).shift(LEFT * 2)

        nodo_b= Circle(radius= 0.45)
        etiqueta_b= Text("B", font_size=36).move_to(nodo_b.get_center())
        grupo_b = VGroup(nodo_b,etiqueta_b).shift(RIGHT * 2)

        #una arista simple (linea entre los centros)
        arista = Line(nodo_a.get_right(), nodo_b.get_left())
        arista.z_index = -1
        self.play(Create(grupo_a))
        self.play(Create(grupo_b))
        self.play(Create(arista))
        self.wait(1.2)

        self.play(FadeOut(VGroup(titulo, subtitulo, grupo_a, grupo_b, arista)))

