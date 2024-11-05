from manim import *

class CreateCircle(Scene):
    def construct(self):
        circle = Circle()
        # circle.set_fill(RED, opacity=0.5)
        self.play(Create(circle))

class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()

        square.rotate(PI / 4)

        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(color=WHITE, width=4)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.wait(1)
        self.play(FadeOut(square))

class SquareAndCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()

        circle.set_fill(RED, opacity=0.5)
        square.set_fill(BLUE, opacity=0.5)

        square.next_to(circle, UP, buff=0)
        self.play(Create(circle), Create(square))

class AnimatedSquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()

        self.play(Create(square))
        self.play(square.animate.rotate(PI / 4))
        self.play(Transform(square, circle))
        self.play(
            square.animate.set_fill(BLUE, opacity=0.5),
        )

class DifferentRotations(Scene):
    def construct(self):
        left = Square(color=BLUE, fill_opacity=0.5).shift(2 * LEFT)
        right = Square(color=RED, fill_opacity=0.5).shift(2 * RIGHT)

        self.play(
            left.animate.rotate(PI),
            Rotate(right, angle=PI),
            run_time = 2
        )
        self.wait()

class TwoTransforms(Scene):
    def transform(self):
        a = Circle()
        b = Square()
        c = Triangle()
        self.play(Transform(a, b))
        self.play(Transform(a, c))
        self.play(FadeOut(a))

    def replacement_transform(self):
        a = Circle()
        b = Square()
        c = Triangle()
        self.play(ReplacementTransform(a, b))
        self.play(ReplacementTransform(b, c))
        self.play(FadeOut(c))

    def construct(self):
        self.transform()
        self.wait(0.5)  # wait for 0.5 seconds
        self.replacement_transform()

class TextHelloWorld(Scene):
    def construct(self):
        static_text = Text("Hello, World!")
        static_text.scale(2)
        static_text.shift(2 * UP)
        self.add(static_text)
        self.wait(1)

        written_text = Text("Hello, World!")
        written_text.scale(2)
        self.play(Write(written_text))
        self.play(written_text.animate.to_edge(DOWN))
        self.play(FadeOut(written_text))

    