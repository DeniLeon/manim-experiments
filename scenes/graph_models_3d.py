from manim import *
import numpy as np
import random
from itertools import combinations


# =========================================================
# Utilidades
# =========================================================

def generate_points_3d(n, scale=2.5, seed=7):
    random.seed(seed)
    np.random.seed(seed)

    points = []
    for _ in range(n):
        x = np.random.uniform(-scale, scale)
        y = np.random.uniform(-scale, scale)
        z = np.random.uniform(-scale, scale)
        points.append(np.array([x, y, z]))
    return points


def make_nodes(points, radius=0.08, color=BLUE_E):
    nodes = VGroup()
    for p in points:
        nodes.add(Dot3D(point=p, radius=radius, color=color))
    return nodes


def make_edges(points, edges, color=WHITE, stroke_width=2):
    edge_group = VGroup()
    for i, j in edges:
        edge_group.add(
            Line(
                start=points[i],
                end=points[j],
                color=color,
                stroke_width=stroke_width
            )
        )
    return edge_group


# =========================================================
# Modelos generadores
# =========================================================

def gnm_edges(n, m, seed=1):
    random.seed(seed)
    all_possible = list(combinations(range(n), 2))
    chosen = random.sample(all_possible, min(m, len(all_possible)))
    return chosen


def gnp_edges(n, p, seed=2):
    random.seed(seed)
    edges = []
    for i, j in combinations(range(n), 2):
        if random.random() < p:
            edges.append((i, j))
    return edges


def geographic_edges(points, radius=1.9):
    edges = []
    n = len(points)
    for i, j in combinations(range(n), 2):
        dist = np.linalg.norm(points[i] - points[j])
        if dist <= radius:
            edges.append((i, j))
    return edges


def dorogovtsev_mendes_steps(num_new_nodes, seed=3):
    random.seed(seed)
    np.random.seed(seed)

    positions = [
        np.array([-1.2, -0.7, 0.0]),
        np.array([1.2, -0.7, 0.0]),
        np.array([0.0, 1.1, 0.4]),
    ]

    edges = [(0, 1), (1, 2), (2, 0)]
    steps = []

    for new_idx in range(3, 3 + num_new_nodes):
        chosen_edge = random.choice(edges)
        u, v = chosen_edge

        midpoint = (positions[u] + positions[v]) / 2
        jitter = np.array([
            np.random.uniform(-0.5, 0.5),
            np.random.uniform(-0.5, 0.5),
            np.random.uniform(-0.4, 0.4),
        ])

        new_pos = midpoint + jitter
        positions.append(new_pos)

        new_edges = [(new_idx, u), (new_idx, v)]
        steps.append((new_idx, new_edges))
        edges.extend(new_edges)

    return positions, edges, steps


# =========================================================
# Clase base reutilizable
# =========================================================

class GraphModelsBase(ThreeDScene):
    def setup_scene(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.08)

    def show_title(self, title_text, subtitle_text=""):
        title = Text(title_text, font_size=34).to_edge(UP)

        if subtitle_text:
            subtitle = Text(subtitle_text, font_size=24).next_to(title, DOWN)
            group = VGroup(title, subtitle)
        else:
            group = VGroup(title)

        self.add_fixed_in_frame_mobjects(group)
        self.play(FadeIn(group, shift=DOWN), run_time=1)
        return group

    def intro_scene(self):
        title = Text("Modelos generadores de grafos en 3D", font_size=44)
        title.to_edge(UP)

        modelos = [
            ("Erdős–Rényi", BLUE),
            ("Gilbert", GREEN),
            ("Geográfico", ORANGE),
            ("Dorogovtsev–Mendes", PURPLE),
        ]

        boxes = VGroup()

        for nombre, color in modelos:
            texto = Text(nombre, font_size=26)

            box = RoundedRectangle(
                corner_radius=0.18,
                height=1.0,
                width=texto.width + 0.7,
                stroke_color=color,
                stroke_width=3,
                fill_color=color,
                fill_opacity=0.12,
            )

            texto.move_to(box.get_center())
            grupo = VGroup(box, texto)
            boxes.add(grupo)

        boxes.arrange(RIGHT, buff=0.35)
        # boxes.arrange_in_grid(rows=2, cols=2, buff=(0.45, 0.35))
        boxes.scale(0.95)
        boxes.next_to(title, DOWN, buff=0.9)

        self.play(Write(title), run_time=1.2)
        self.remove(title)
        self.add_fixed_in_frame_mobjects(title)

        for b in boxes:
            b.set_opacity(0)

        self.add_fixed_in_frame_mobjects(boxes)

        self.play(
            LaggedStart(
                *[b.animate.set_opacity(1) for b in boxes],
                lag_ratio=0.3
            ),
            run_time=2.8
        )

        self.wait(2)
        self.play(FadeOut(title), FadeOut(boxes), run_time=1)

    def gnm_scene(self):
        label = self.show_title("1. G(n,m) de Erdős–Rényi", "n = 8, m = 10")

        points = generate_points_3d(8, scale=2.3, seed=10)
        nodes = make_nodes(points, radius=0.07, color=BLUE_D)

        self.play(
            LaggedStart(*[FadeIn(node, scale=0.5) for node in nodes], lag_ratio=0.08),
            run_time=1.8
        )

        edges = gnm_edges(8, 10, seed=14)
        edge_mobjects = [make_edges(points, [e], color=GRAY_C, stroke_width=2) for e in edges]

        self.play(
            LaggedStart(*[Create(edge) for edge in edge_mobjects], lag_ratio=0.12),
            run_time=2.5
        )

        self.wait(1.5)

        self.play(
            FadeOut(nodes),
            *[FadeOut(edge) for edge in edge_mobjects],
            FadeOut(label),
            run_time=1
        )

    def gnp_scene(self):
        label = self.show_title("2. G(n,p) de Gilbert", "n = 8, p = 0.35")

        points = generate_points_3d(8, scale=2.3, seed=20)
        nodes = make_nodes(points, radius=0.07, color=TEAL_D)

        self.play(
            LaggedStart(*[FadeIn(node, scale=0.5) for node in nodes], lag_ratio=0.08),
            run_time=1.8
        )

        edges = gnp_edges(8, 0.35, seed=21)
        edge_mobjects = [make_edges(points, [e], color=GRAY_C, stroke_width=2) for e in edges]

        self.play(
            LaggedStart(*[Create(edge) for edge in edge_mobjects], lag_ratio=0.09),
            run_time=2.6
        )

        self.wait(1.5)

        self.play(
            FadeOut(nodes),
            *[FadeOut(edge) for edge in edge_mobjects],
            FadeOut(label),
            run_time=1
        )

    def geographic_scene(self):
        label = self.show_title("3. Modelo geográfico", "Conectar si la distancia ≤ r")

        points = generate_points_3d(10, scale=2.2, seed=30)
        nodes = make_nodes(points, radius=0.07, color=GREEN_D)

        self.play(
            LaggedStart(*[FadeIn(node, scale=0.5) for node in nodes], lag_ratio=0.08),
            run_time=1.8
        )

        edges = geographic_edges(points, radius=1.9)
        edge_mobjects = [make_edges(points, [e], color=GRAY_C, stroke_width=2) for e in edges]

        self.play(
            LaggedStart(*[Create(edge) for edge in edge_mobjects], lag_ratio=0.08),
            run_time=2.5
        )

        self.wait(1.5)

        self.play(
            FadeOut(nodes),
            *[FadeOut(edge) for edge in edge_mobjects],
            FadeOut(label),
            run_time=1
        )

    def dm_scene(self):
        label = self.show_title("4. Dorogovtsev–Mendes", "Crecimiento sobre aristas")

        positions, final_edges, steps = dorogovtsev_mendes_steps(num_new_nodes=6, seed=40)

        initial_nodes = make_nodes(positions[:3], radius=0.07, color=PURPLE_D)
        initial_edges = make_edges(
            positions,
            [(0, 1), (1, 2), (2, 0)],
            color=GRAY_C,
            stroke_width=2
        )

        self.play(FadeIn(initial_nodes), Create(initial_edges), run_time=1.8)

        all_new_nodes = VGroup()
        all_new_edges = VGroup()

        for new_idx, new_edges in steps:
            new_node = Dot3D(point=positions[new_idx], radius=0.07, color=PURPLE_D)
            new_edge_mobs = make_edges(positions, new_edges, color=GRAY_C, stroke_width=2)

            self.play(
                FadeIn(new_node, scale=0.5),
                LaggedStart(*[Create(edge) for edge in new_edge_mobs], lag_ratio=0.15),
                run_time=0.9
            )

            all_new_nodes.add(new_node)
            all_new_edges.add(*new_edge_mobs)

        self.wait(1.5)

        self.play(
            FadeOut(initial_nodes),
            FadeOut(initial_edges),
            FadeOut(all_new_nodes),
            FadeOut(all_new_edges),
            FadeOut(label),
            run_time=1
        )

    def outro_scene(self):
        text = Text("Distintas reglas de generación.", font_size=32).to_edge(UP)

        self.add_fixed_in_frame_mobjects(text)
        self.play(FadeIn(text), run_time=1)
        self.wait(2)
        self.play(FadeOut(text), run_time=1)


# =========================================================
# Escena completa
# =========================================================

class GraphModels3D(GraphModelsBase):
    def construct(self):
        self.setup_scene()
        self.intro_scene()
        self.gnm_scene()
        self.gnp_scene()
        self.geographic_scene()
        self.dm_scene()
        self.outro_scene()


# =========================================================
# Previews individuales
# =========================================================

class IntroPreview(GraphModelsBase):
    def construct(self):
        self.setup_scene()
        self.intro_scene()


class GnmPreview(GraphModelsBase):
    def construct(self):
        self.setup_scene()
        self.gnm_scene()


class GnpPreview(GraphModelsBase):
    def construct(self):
        self.setup_scene()
        self.gnp_scene()


class GeographicPreview(GraphModelsBase):
    def construct(self):
        self.setup_scene()
        self.geographic_scene()


class DMPreview(GraphModelsBase):
    def construct(self):
        self.setup_scene()
        self.dm_scene()


class OutroPreview(GraphModelsBase):
    def construct(self):
        self.setup_scene()
        self.outro_scene()