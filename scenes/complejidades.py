from manim import *
import numpy as np


class ComplejidadesCrecen(Scene):
    def construct(self):
        # 1) Ejes
        axes = Axes(
            x_range=[1, 20, 1],
            y_range=[0, 260, 50],
            x_length=10,
            y_length=5.5,
            tips=False,
        ).to_edge(DOWN)

        x_label = axes.get_x_axis_label(Text("n", font_size=20))
        y_label = axes.get_y_axis_label(Text("costo", font_size=20))

        titulo = Text("Complejidad", font_size=44).to_edge(UP)

        self.play(FadeIn(titulo))
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label))

    
        def f_const(n):   return 6
        def f_log(n):     return 6 * np.log2(n)
        def f_n(n):       return 3 * n
        def f_nlogn(n):   return 2.0 * n * np.log2(n)
        def f_n2(n):      return 0.6 * (n ** 2)

        curves = [
            ("O(1)", f_const),
            ("O(log n)", f_log),
            ("O(n)", f_n),
            ("O(n log n)", f_nlogn),
            ("O(n²)", f_n2),
        ]

        # 3) Tracker: controla hasta qué n vamos dibujando
        n_tracker = ValueTracker(1)

        # 4) Curvas que se redibujan automáticamente conforme crece n_tracker
        plotted = []
        labels = []

        for name, func in curves:
            graph = always_redraw(
                lambda func=func: axes.plot(
                    func,
                    x_range=[1, n_tracker.get_value()],
                )
            )
            plotted.append(graph)

            # Etiqueta pegada al final de la curva (en x = n_tracker)
            label = always_redraw(
                lambda name=name, func=func: Text(name, font_size=20).next_to(
                    axes.c2p(n_tracker.get_value(), func(n_tracker.get_value())),
                    RIGHT,
                    buff=0.2,
                )
            )
            labels.append(label)

        # 5) Un “cursor” vertical para que se note el n actual
        cursor = always_redraw(
            lambda: axes.get_vertical_line(
                axes.c2p(n_tracker.get_value(), 0),
                line_func=Line,
            ).set_stroke(width=3)
        )

        # 6) Mostrar todo (curvas + etiquetas + cursor)
        self.play(*[Create(g) for g in plotted], FadeIn(cursor), *[FadeIn(l) for l in labels])
        self.wait(0.5)

        # 7) Animación principal: crecer n de 1 a 20
        self.play(n_tracker.animate.set_value(20), run_time=6, rate_func=linear)
        self.wait(1)

        # 8) Cierre: enfatiza el “boom” de n^2 con un zoom leve a la derecha (opcional)
        #self.play(self.camera.frame.animate.scale(0.95).shift(RIGHT * 1.2), run_time=1.2)
       #self.wait(1)