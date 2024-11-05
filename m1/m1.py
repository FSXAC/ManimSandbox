# Animates the M1 chip animation

from manim import *

class Box:
    def __init__(self, num_sub_boxes=1, flip=False):
        self.num_sub_boxes = num_sub_boxes
        self.flip = flip

        self.sub_boxes = {}
        self.sub_box_weights = [1] * num_sub_boxes

    def addSubBox(self, index, **kwargs):

        index = index % self.num_sub_boxes
        
        self.sub_boxes[index] = Box(**kwargs)
        return self.sub_boxes[index]
    
    def setSubBoxWeight(self, index, weight):
        index = index % self.num_sub_boxes
        self.sub_box_weights[index] = weight

    def createObjs(self, width, height, draw_outer_box=True):
        group = VGroup()

        box = Rectangle(width=width, height=height)
        if not draw_outer_box:
            box.set_stroke(opacity=0)
        else:
            box.set_stroke(width=1, opacity=0.7)
        group.add(box)

        if self.num_sub_boxes > 1:

            # draw division lines for num of subboxes
            length = height if self.flip else width
            inc_dir = DOWN if self.flip else RIGHT

            # Uniform spacing
            spacing_uniform = length / self.num_sub_boxes
            print(f'Uniform spacing: {spacing_uniform}')

            # Compute weights
            norm_weights = [w / sum(self.sub_box_weights) for w in self.sub_box_weights]
            print(norm_weights)
            print(sum(norm_weights)) # Should be 1

            # Calulate spacing
            spacing = [spacing_uniform] * self.num_sub_boxes
            for i, w in enumerate(norm_weights):
                spacing[i] = w * length

            print(spacing)

            for i in range(self.num_sub_boxes - 1):
                spacing_i = sum(spacing[:i + 1])
                start = box.get_corner(UL) + inc_dir * spacing_i
                if self.flip:
                    end = box.get_corner(UR) + inc_dir * spacing_i
                else:
                    end = box.get_corner(DL) + inc_dir * spacing_i
                l = Line(start=start, end=end)
                l.set_stroke(width=1, opacity=0.5)
                group.add(l)

            # draw sub boxes
            for i in range(self.num_sub_boxes):
                if i not in self.sub_boxes:
                    continue

                sub_box_width = width if self.flip else spacing[i]
                sub_box_height = spacing[i] if self.flip else height
                sub_box = self.sub_boxes[i].createObjs(sub_box_width, sub_box_height, draw_outer_box=False)
                # sub_box.set_stroke(width=1, opacity=0.5)

                sub_box_ul = box.get_corner(UL) + (inc_dir * sum(spacing[:i]))
                sub_box.align_to(sub_box_ul, UL)
                group.add(sub_box)

        return group
class M1(Scene):


    def construct(self):
        self.square = Square(side_length=6)
        self.outer_square = Square(side_length=6.1, color=WHITE, fill_opacity=0)
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
            *self.animate_top_right(),
            *self.animate_bottom_left(),
            *self.animate_bottom_right(),
        )

        # self.play(
            
        # )
        apple_logo = Text("")
        apple_logo.scale(3)

        self.play(
            FadeOut(*self.objs, run_time=0.3),
            CounterclockwiseTransform(self.outer_square, apple_logo)
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
    
    def animate_bottom_left(self):

        # instead of drawing boxes manually, let's build a tree of boxes
        # and write a function to programmatically draw them

        QUAD_WIDTH = self.square.get_width() / 2
        QUAD_HEIGHT = QUAD_WIDTH
        QUAD_UL = self.square.get_edge_center(LEFT)
        
        ll = Box(num_sub_boxes=2, flip=True)
        ll.setSubBoxWeight(-1, 2)

        NUM_E_CORES = 4
        e_cores = ll.addSubBox(0, num_sub_boxes=NUM_E_CORES)
        for i in range(NUM_E_CORES):
            e_core = e_cores.addSubBox(i, num_sub_boxes=3)
            e_core.setSubBoxWeight(1, 2)

            core = e_core.addSubBox(1, num_sub_boxes=5, flip=True)
            core.setSubBoxWeight(0, 3)  # top
            core.setSubBoxWeight(-1, 3) # bot
            core.setSubBoxWeight(2, 3)

            core.addSubBox(0, num_sub_boxes=5)
            core.addSubBox(-1, num_sub_boxes=5)
        
        # Neural engines
        NUM_NPU_ROWS = 2
        NUM_NPU_COLS = 8
        npus = ll.addSubBox(1, num_sub_boxes=NUM_NPU_ROWS, flip=True)
        for i in range(NUM_NPU_ROWS):
            npu_row = npus.addSubBox(i, num_sub_boxes=NUM_NPU_COLS)
            for j in range(NUM_NPU_COLS):
                npu = npu_row.addSubBox(j, num_sub_boxes=4)
                for k in range(4):
                    npu_core = npu.addSubBox(k, num_sub_boxes=4, flip=True)
                    if k in [1, 2]:
                        npu_core.addSubBox(1, num_sub_boxes=8, flip=True)
                        npu_core.addSubBox(2, num_sub_boxes=8, flip=True)

                
            

        ll_objs = ll.createObjs(QUAD_WIDTH, QUAD_HEIGHT)
        ll_objs.align_to(QUAD_UL, UL)

        self.objs += ll_objs
        return [Create(ll_objs)]
    
    def animate_bottom_right(self):
        QUAD_WIDTH = self.square.get_width() / 2
        QUAD_HEIGHT = QUAD_WIDTH
        QUAD_UR = self.square.get_edge_center(RIGHT)

        lr = Box(num_sub_boxes=2, flip=True)

        secure_enclave = lr.addSubBox(0, num_sub_boxes=2)
        se_left = secure_enclave.addSubBox(0, num_sub_boxes=2, flip=True)
        engine = se_left.addSubBox(0, num_sub_boxes=7)
        engine.setSubBoxWeight(1, 3)
        engine.setSubBoxWeight(-2, 3)
        engine.setSubBoxWeight(3, 10)
        engine.addSubBox(0, num_sub_boxes=20, flip=True)
        engine.addSubBox(-1, num_sub_boxes=20, flip=True)

        engine_core = engine.addSubBox(3, num_sub_boxes=5, flip=True)
        engine_core_centre = engine_core.addSubBox(2, num_sub_boxes=11)
        engine_core_centre.setSubBoxWeight(0, 3)
        engine_core_centre.setSubBoxWeight(-1, 3)
        engine_core_centre.addSubBox(4, num_sub_boxes=4)
        engine_core_centre.addSubBox(6, num_sub_boxes=4)

        engine_peripheral = se_left.addSubBox(1, num_sub_boxes=2)
        crypto = engine_peripheral.addSubBox(0, num_sub_boxes=5)
        crypto.setSubBoxWeight(2, 7)
        crypto_core = crypto.addSubBox(2, num_sub_boxes=5, flip=True)
        crypto_core.addSubBox(0, num_sub_boxes=12)
        crypto_core.addSubBox(-1, num_sub_boxes=12)
        crypto_core_centre = crypto_core.addSubBox(2, num_sub_boxes=3)
        crypto_core_centre.setSubBoxWeight(1, 0.7)
        crypto_core_centre.addSubBox(0, num_sub_boxes=2, flip=True)
        crypto_core_centre.addSubBox(-1, num_sub_boxes=2, flip=True)

        aux_cores = engine_peripheral.addSubBox(1, num_sub_boxes=2, flip=True)
        aux_top = aux_cores.addSubBox(0, num_sub_boxes=2)

        misc1 = aux_top.addSubBox(0, num_sub_boxes=3)
        misc1.addSubBox(-1, num_sub_boxes=6, flip=True)
        misc1_centre = misc1.addSubBox(1, num_sub_boxes=3, flip=True)
        misc1_centre.addSubBox(1, num_sub_boxes=3)

        misc2 = aux_top.addSubBox(-1, num_sub_boxes=3, flip=True)
        misc2.setSubBoxWeight(1, 1.5)
        misc2_centre = misc2.addSubBox(1, num_sub_boxes=3)
        misc2_centre.addSubBox(1, num_sub_boxes=5, flip=True)

        aux_bot = aux_cores.addSubBox(1, num_sub_boxes=3, flip=True)
        aux_bot_centre = aux_bot.addSubBox(1, num_sub_boxes=3)
        aux_bot_centre.setSubBoxWeight(1, 2)
        aux_bot_centre.addSubBox(0, num_sub_boxes=5)
        aux_bot_centre.addSubBox(-1, num_sub_boxes=5)
        aux_bot_centre.addSubBox(1, num_sub_boxes=2, flip=True)

        se_right = secure_enclave.addSubBox(1, num_sub_boxes=3, flip=True)
        se_right.setSubBoxWeight(0, 1)
        se_right.setSubBoxWeight(1, 3)
        se_right.setSubBoxWeight(2, 24)
        se_io_top = se_right.addSubBox(1, num_sub_boxes=32)
        se_io_top.setSubBoxWeight(-1, 8)

        se_io_main = se_right.addSubBox(2, num_sub_boxes=2)
        se_io_main.setSubBoxWeight(-1, 0.25)
        se_io_main.addSubBox(1, num_sub_boxes=32, flip=True)

        se_io_core = se_io_main.addSubBox(0, num_sub_boxes=5)
        se_io_core.setSubBoxWeight(1, 0.5)
        se_io_core.setSubBoxWeight(2, 2)
        se_io_core.setSubBoxWeight(3, 0.5)
        se_io_core_left = se_io_core.addSubBox(0, num_sub_boxes=5, flip=True)
        se_io_core_left.setSubBoxWeight(0, 3)
        se_io_core_left.setSubBoxWeight(-1, 3)
        se_io_core_right = se_io_core.addSubBox(-1, num_sub_boxes=5, flip=True)
        se_io_core_right.setSubBoxWeight(0, 3)
        se_io_core_right.setSubBoxWeight(-1, 3)
        se_io_core_centre = se_io_core.addSubBox(2, num_sub_boxes=3, flip=True)
        se_io_core_centre.setSubBoxWeight(1, 0.2)
        se_io_core_centre.addSubBox(0, num_sub_boxes=2)
        se_io_core_centre.addSubBox(-1, num_sub_boxes=2)

        media = lr.addSubBox(1, num_sub_boxes=5, flip=True)
        media.setSubBoxWeight(2, 3)
        media_core = media.addSubBox(2, num_sub_boxes=5)
        media_core.setSubBoxWeight(0, 2)
        media_core.setSubBoxWeight(1, 1)
        media_core.setSubBoxWeight(2, 3)
        media_core.setSubBoxWeight(3, 1)
        media_core.setSubBoxWeight(-1, 2)

        m_out_left = media_core.addSubBox(0, num_sub_boxes=7, flip=True)
        m_out_left.setSubBoxWeight(3, 3)
        m_out_right = media_core.addSubBox(-1, num_sub_boxes=7, flip=True)
        m_out_right.setSubBoxWeight(3, 3)

        media_core.addSubBox(1, num_sub_boxes=20, flip=True)
        media_core.addSubBox(3, num_sub_boxes=20, flip=True)
        media_core_centre = media_core.addSubBox(2, num_sub_boxes=5, flip=True)
        media_core_centre.addSubBox(1, num_sub_boxes=20)
        media_core_centre.addSubBox(3, num_sub_boxes=20)

        lr_objs = lr.createObjs(QUAD_WIDTH, QUAD_HEIGHT)
        lr_objs.align_to(QUAD_UR, UR)

        self.objs += lr_objs
        
        return [Create(lr_objs)]