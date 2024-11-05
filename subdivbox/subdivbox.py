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
                l.set_stroke(color=RED)
                group.add(l)

            # draw sub boxes
            for i in range(self.num_sub_boxes):
                if i not in self.sub_boxes:
                    continue

                sub_box_width = width if self.flip else spacing[i]
                sub_box_height = spacing[i] if self.flip else height
                sub_box = self.sub_boxes[i].createObjs(sub_box_width, sub_box_height, draw_outer_box=False)
                sub_box.set_stroke(color=BLUE)

                sub_box_ul = box.get_corner(UL) + (inc_dir * sum(spacing[:i]))
                sub_box.align_to(sub_box_ul, UL)
                group.add(sub_box)

        return group

class SubDivBox(Scene):
    def construct(self):

        # Create title
        title = Text("Sub-div box")
        title.align_on_border(UL)

        self.add(title)

        box = Box(num_sub_boxes=3, flip=False)
        box.setSubBoxWeight(0, 1)
        box.setSubBoxWeight(1, 2)
        box_s1 = box.addSubBox(0, num_sub_boxes=5, flip=True)
        box_s2 = box.addSubBox(-1, num_sub_boxes=5, flip=True)
        box_s3 = box.addSubBox(1, num_sub_boxes=2)

        box_s1.addSubBox(1, num_sub_boxes=10, flip=False)
        box_s1.addSubBox(-2, num_sub_boxes=10, flip=False)


        box_objs = box.createObjs(4, 4)

        # self.play(Create(box_objs), run_time=3)
        self.add(box_objs)