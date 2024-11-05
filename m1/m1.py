# Animates the M1 chip animation

from manim import *

class M1(Scene):


    def construct(self):
        self.square = Square(side_length=4)
        self.outer_square = Square(side_length=4.1, color=WHITE, fill_opacity=0)
        self.outer_square.set_stroke(width=10)
        
        self.objs = []

        self.play(Create(self.outer_square))

        # subdivide the square into 4 smaller squares
        # lines = [
        #     Line(start=self.outer_square.get_edge_center(UP), end=self.outer_square.get_corner(DOWN)),
        #     Line(start=self.outer_square.get_corner(LEFT), end=self.outer_square.get_corner(RIGHT))
        # ]
        # for line in lines:
        #     line.set_stroke(width=2)

        # self.play(Create(lines[0]), Create(lines[1]))

        # self.draw_top_left()
        # self.draw_top_right()
        # self.draw_bottom_left()
        # self.draw_bottom_right()

        self.play(
            *self.animate_top_left(),
            *self.animate_top_right()
        )

        # self.play(
            
        # )
        apple_logo = Text("")
        apple_logo.scale(3)

        self.play(
            FadeOut(*self.objs, run_time=0.3),
            Transform(self.outer_square, apple_logo)
        )

        self.play(
            FadeOut(self.outer_square)
        )


    def animate_top_left(self):

        animations = []

        l1 = Line(start=self.square.get_edge_center(LEFT), end=self.square.get_edge_center(RIGHT))
        l1.stroke_width = 2
        l2 = Line(start=self.square.get_edge_center(UP), end=self.square.get_edge_center(DOWN))
        l2.stroke_width = 2
        animations += [Create(l1), Create(l2)]
        self.objs += [l1, l2]

        # draw apple logo and M1 text
        tl_text = Text("M1", font="Arial")
        tl_text.scale(0.7)
        tl_text.align_to(self.square, UL)
        tl_text.shift(DOWN * 0.08 + RIGHT * 0.08)
        animations.append(Write(tl_text))
        self.objs.append(tl_text)

        # p-core height
        num_p_cores = 4
        p_core_height = (self.square.get_height() / 2) * (2/3)
        p_core_width  = (self.square.get_width() / 2) / num_p_cores
        p_cores = []

        for i in range(num_p_cores):
            p_core = Rectangle(height=p_core_height, width=p_core_width)
            p_core.set_stroke(width=2)
            if i == 0:
                p_core.move_to(self.square.get_edge_center(LEFT) + UP * p_core_height / 2 + RIGHT * p_core_width / 2)
            else:
                p_core.next_to(p_cores[i-1], RIGHT, buff=0)
            p_cores.append(p_core)
            animations.append(Create(p_core, run_time=(1 + 0.2 * i)))

            # Add details
            margin_perc = 0.2
            line_top = Line(start=p_core.get_edge_center(LEFT), end=p_core.get_edge_center(RIGHT))
            line_top.align_to(p_core, UP)
            line_top.set_stroke(width=1)
            line_top.shift(DOWN * p_core_height * (margin_perc))
            animations.append(Create(line_top))

            line_bottom = Line(start=p_core.get_edge_center(LEFT), end=p_core.get_edge_center(RIGHT))
            line_bottom.align_to(p_core, DOWN)
            line_bottom.set_stroke(width=1)
            line_bottom.shift(UP * p_core_height * (margin_perc))
            animations.append(Create(line_bottom))

            # Create finer details
            l_margin_perc = 0.2
            l_margin_start = l_margin_perc * p_core_width
            l_margin_end = p_core_width * (1 - l_margin_perc)

            num_v_lines = 6
            v_lines_x = [l_margin_start + (l_margin_end - l_margin_start) / num_v_lines * (j + 0.5) for j in range(num_v_lines)]

            sm_line_margin_perc = 0.1
            # sm_line_top_y = line_top.get_edge_center(UP) + DOWN * (p_core_height * sm_line_margin_perc)
            # sm_line_bottom_y = line_bottom.get_edge_center(DOWN) + UP * (p_core_height * sm_line_margin_perc)
            sm_line_margin = (p_core_height * sm_line_margin_perc)
            sm_line_x1 = v_lines_x[1]
            sm_line_x2 = v_lines_x[-2]
            sm_line_start = line_top.get_corner(UL) + (RIGHT * sm_line_x1) + DOWN * sm_line_margin
            sm_line_stop  = sm_line_start + RIGHT * (sm_line_x2 - sm_line_x1)
            sm_line_top = Line(start=sm_line_start, end=sm_line_stop)
            sm_line_top.set_stroke(width=1, opacity=0.7)
            animations.append(Create(sm_line_top))
            self.objs.append(sm_line_top)

            sm_line_start = line_bottom.get_corner(DL) + (RIGHT * sm_line_x1) + UP * sm_line_margin
            sm_line_stop  = sm_line_start + RIGHT * (sm_line_x2 - sm_line_x1)
            sm_line_bottom = Line(start=sm_line_start, end=sm_line_stop)
            sm_line_bottom.set_stroke(width=1, opacity=0.7)
            animations.append(Create(sm_line_bottom))
            self.objs.append(sm_line_bottom)

            
            v_line_spacing = (l_margin_end - l_margin_start) / num_v_lines
            for j in range(num_v_lines):
                if j in range(2, 4):
                    line = Line(start=line_top.get_edge_center(UP) + DOWN * sm_line_margin, end=line_bottom.get_edge_center(DOWN) + UP * sm_line_margin)
                else:
                    line = Line(start=line_top.get_edge_center(UP), end=line_bottom.get_edge_center(DOWN))
                line.align_to(p_core, LEFT)
                line.set_stroke(width=1, opacity=0.5)
                line.next_to(p_core, RIGHT, buff=l_margin_start + (j + 0.5) * v_line_spacing - p_core_width)
                animations.append(Create(line, run_time = 1.0 + 0.1 * j + 0.1 * i))
                self.objs.append(line)

            self.objs += [line_top, line_bottom]
            self.objs += [p_core]
        
        return animations

    def animate_top_right(self):

        QUAD_WIDTH = self.square.get_width() / 2
        QUAD_HEIGHT = QUAD_WIDTH
        QUAD_UL = self.square.get_edge_center(UP)

        NUM_GPUS = 8
        GPU_WIDTH = QUAD_WIDTH / NUM_GPUS
        GPU_HEIGHT = QUAD_HEIGHT

        # These margins are w.r.t. GPU geometry
        SIDEBAND_MARGIN = GPU_WIDTH * 0.25
        HLINE_SPACING = GPU_HEIGHT * 0.02
        NUM_HLINE = 4
        HLINE_OUTER_MARGIN_FROM_CENTER = GPU_HEIGHT * 0.15

        # first write function to create objects using primitives
        def make_gpu(origin, width, height):

            MID_X_L = origin + DOWN * (height / 2)
            MID_X_R = MID_X_L + RIGHT * width

            # Reference line
            # mid_line_ref = Line(start=MID_X_L, end=MID_X_R)
            # mid_line_ref.set_stroke(width=1, color=RED)
            # objs = [mid_line_ref]
            objs = []

            # rectangle
            gpu_rect = Rectangle(height=GPU_HEIGHT, width=GPU_WIDTH)
            gpu_rect.set_stroke(width=2, opacity=0.5)
            gpu_rect.align_to(origin, UL)
            objs.append(gpu_rect)

            for direction in [UP, DOWN]:
                y_offset = (direction * HLINE_OUTER_MARGIN_FROM_CENTER)
                for n in range(NUM_HLINE):
                    n_offset = n * direction * HLINE_SPACING
                    start = MID_X_L + y_offset + n_offset
                    end = MID_X_R + y_offset + n_offset

                    line = Line(start=start, end=end)
                    line.set_stroke(width=1, opacity=0.5)

                    objs.append(line)

            y_offset = UP * ((NUM_HLINE - 1) / 2) * HLINE_SPACING
            for n in range(NUM_HLINE):
                n_offset = n * DOWN * HLINE_SPACING
                # n_offset = 0
                start = MID_X_L + y_offset + n_offset + RIGHT * SIDEBAND_MARGIN
                end = MID_X_R + y_offset + n_offset + LEFT * SIDEBAND_MARGIN
                line = Line(start=start, end=end)
                line.set_stroke(width=1, opacity=0.5)
                objs.append(line)

            SIDEBAND_ML = MID_X_L + RIGHT * SIDEBAND_MARGIN
            SIDEBAND_MR = MID_X_R + LEFT * SIDEBAND_MARGIN


            # create side bars
            y_start_offset = UP * HLINE_OUTER_MARGIN_FROM_CENTER
            y_end_offset = DOWN * HLINE_OUTER_MARGIN_FROM_CENTER
            for m in [SIDEBAND_ML, SIDEBAND_MR]:
                l = Line(start=m + y_start_offset, end=m + y_end_offset)
                l.set_stroke(width=1, opacity=0.5)
                objs.append(l)

            v_offset = HLINE_OUTER_MARGIN_FROM_CENTER + ((NUM_HLINE - 1) * HLINE_SPACING)
            for dirv in [UP, DOWN]:
                for m in [SIDEBAND_ML, SIDEBAND_MR]:
                    start = m + dirv * v_offset
                    end = start + dirv * (0.5 * height - v_offset)

                    l = Line(start=start, end=end)
                    l.set_stroke(width=1, opacity=0.5)
                    objs.append(l)

            return objs
        

        animations = []

        for gpu_i in range(NUM_GPUS):
            gpu_origin = QUAD_UL + RIGHT * GPU_WIDTH * gpu_i
            gpu_objs = make_gpu(gpu_origin, GPU_WIDTH, GPU_HEIGHT)

            # sort by locations so it looks nice
            gpu_objs_sorted = sorted(gpu_objs, key=lambda obj: obj.get_center()[0] * obj.get_center()[1], reverse=True)
            animations += [Create(o, run_time=1.0 + (0.03 * i) + (0.05 * gpu_i)) for i,o in enumerate(gpu_objs_sorted)]

            self.objs += gpu_objs

        return animations