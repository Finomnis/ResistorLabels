from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import black, toColor, HexColor

import math


pdfmetrics.registerFont(TTFont('Arial Bold', 'ArialBd.ttf'))


class StickerRect:
    def __init__(self, row, column):
        self.left = (3/16 + (2+6/8) * column) * inch
        self.bottom = (11 - (1.5 + row)) * inch
        self.width = (2+5/8) * inch
        self.height = 1*inch
        self.corner = 0.1*inch


class ResistorValue:
    def __init__(self, ohms):
        # Fixed-point value with 2 decimals precision
        ohms_exp = math.floor(math.log10(ohms))
        ohms_val = round(ohms / math.pow(10, ohms_exp - 2))
        ohms_exp -= 2

        while ohms_val >= 1000:
            ohms_exp += 1
            ohms_val //= 10

        self.ohms_val = ohms_val
        self.ohms_exp = ohms_exp + 2

        print(self.ohms_val, self.ohms_exp, self.format_value(), self.get_value())

    def get_value(self):
        return self.ohms_val * math.pow(10, self.ohms_exp - 2)

    def get_prefix(self):
        if self.ohms_exp >= 12:
            return "T"
        if self.ohms_exp >= 9:
            return "G"
        if self.ohms_exp >= 6:
            return "M"
        if self.ohms_exp >= 3:
            return "k"
        if self.ohms_exp >= 0:
            return ""
        if self.ohms_exp >= -3:
            return "m"
        if self.ohms_exp >= -6:
            return "\u03BC"
        return "n"

    def get_prefixed_number(self):
        if self.ohms_exp % 3 == 0:
            if self.ohms_val % 100 == 0:
                return str(self.ohms_val // 100)
            elif self.ohms_val % 10 == 0:
                return str(self.ohms_val // 100) + "." + str((self.ohms_val % 100) // 10)
            else:
                return str(self.ohms_val // 100) + "." + str(self.ohms_val % 100)
        elif self.ohms_exp % 3 == 1:
            if self.ohms_val % 10 == 0:
                return str(self.ohms_val // 10)
            else:
                return str(self.ohms_val // 10) + "." + str(self.ohms_val % 10)
        else:
            return str(self.ohms_val)

    def format_value(self):
        return self.get_prefixed_number() + self.get_prefix()


def resistor_color_table_1(num):
    return [
        HexColor("#030303"),
        HexColor("#6f5500"),
        HexColor("#ff0000"),
        HexColor("#f07f00"),
        HexColor("#ffff00"),
        HexColor("#00c200"),
        HexColor("#285fdd"),
        HexColor("#b236a0"),
        HexColor("#b2b2b2"),
        HexColor("#fefefe"),
    ][num]


def resistor_color_table_2(num):
    return [
        HexColor("#000000"),
        HexColor("#994d00"),  # HexColor("#996633"),
        HexColor("#FF0000"),
        HexColor("#FF9900"),
        HexColor("#FFFF00"),
        HexColor("#00FF00"),
        HexColor("#0000FF"),
        HexColor("#FF00FF"),
        HexColor("#CCCCCC"),
        HexColor("#FFFFFF"),
    ][num]


def resistor_color_table_3(num):
    return [
        HexColor("#995817"),
        HexColor("#FF9900"),  # HexColor("#996633"),
        HexColor("#994d00"),
        HexColor("#995c1f"),
        HexColor("#996026"),
        HexColor("#000000"),
        HexColor("#995008"),
        HexColor("#996633"),
        HexColor("#CCCCCC"),
        HexColor("#FFFFFF"),
    ][num]

def draw_resistor_colorcode(c, value, color1, color2, x, y, width, height, num_codes):

    border = height/6
    corner = (height-2*border)/4

    c.saveState()
    p = c.beginPath()
    p.roundRect(x+border, y+border, width-2*border, height-2*border, corner)
    c.clipPath(p, stroke=0)
    c.linearGradient(x+width/2, y+border+height, x+width/2, y+border, (color1, color2))
    c.restoreState()

    width_without_corner = width - 2*border - 2*corner
    stripe_width = width_without_corner/10

    for i in range(num_codes):

        if i == num_codes - 1:
            stripe_value = value.ohms_exp + 2 - num_codes
        else:
            stripe_value = value.ohms_val
            for _ in range(2-i):
                stripe_value //= 10
            stripe_value %= 10

        if stripe_value >= 0:
            c.setFillColor(resistor_color_table_2(stripe_value))
            c.rect(x+border+corner + stripe_width/2 + 2*stripe_width*i, y+border, stripe_width, height-2*border,
                   fill=1, stroke=0)
        else:
            pass

    c.setFillColor(black)

    c.setStrokeColor(black, 1)
    c.setLineWidth(0.5)
    c.roundRect(x+border, y+border, width-2*border, height-2*border, corner)


def draw_resistor_sticker(c, row, column, ohms):
    rect = StickerRect(row, column)

    # Draw middle line
    c.setStrokeColor(black, 0.25)
    c.setLineWidth(0.7)
    c.line(rect.left,
           rect.bottom + rect.height/2,
           rect.left + rect.width,
           rect.bottom + rect.height/2)

    # Draw resistor value
    resistor_value = ResistorValue(ohms)

    value_font_size = 0.25 * inch
    ohm_font_size = 0.15 * inch
    space_between = 5

    value_string = resistor_value.format_value()
    ohm_string = "\u2126"
    value_width = c.stringWidth(value_string, 'Arial Bold', value_font_size * 1.35)
    ohm_width = c.stringWidth(ohm_string, 'Arial Bold', ohm_font_size * 1.35)
    total_text_width = ohm_width + value_width + space_between
    text_left = rect.left + rect.width/4 - total_text_width/2
    text_bottom = rect.bottom + rect.height/4 - value_font_size/2

    c.setFont('Arial Bold', value_font_size * 1.35)
    c.drawString(text_left, text_bottom, value_string)
    c.setFont('Arial Bold', ohm_font_size * 1.35)
    c.drawString(text_left + value_width + space_between, text_bottom, ohm_string)

    # Draw resistor color code
    draw_resistor_colorcode(c, resistor_value,
                            # HexColor("#eeeeee"),  HexColor("#888888"),
                            # HexColor("#e7e1d8"),  HexColor("#ede7de"),
                            # HexColor("#d7cf79"),  HexColor("#d7cf79"),
                            # toColor("hsl(55, 54%, 66%)"), toColor("hsl(55, 54%, 66%)"),
                            # toColor("hsl(55, 54%, 82%)"), toColor("hsl(55, 54%, 50%)"),
                            toColor("hsl(55, 54%, 100%)"), toColor("hsl(55, 54%, 70%)"),
                            rect.left + rect.width/2,
                            rect.bottom + rect.height/4,
                            rect.width/4, rect.height/4,
                            3)

    draw_resistor_colorcode(c, resistor_value,
                            # HexColor("#eeeeee"),  HexColor("#888888"),
                            # HexColor("#e7e1d8"),  HexColor("#ede7de"),
                            # HexColor("#f9f3e9"),  HexColor("#beb8af"),
                            # toColor("hsl(197, 59%, 69%)"), toColor("hsl(197, 59%, 69%)"),
                            # toColor("hsl(197, 59%, 85%)"), toColor("hsl(197, 59%, 60%)"),
                            toColor("hsl(197, 59%, 100%)"), toColor("hsl(197, 59%, 73%)"),
                            rect.left + rect.width * 0.75,
                            rect.bottom + rect.height/4,
                            rect.width/4, rect.height/4,
                            4)


def main():

    c = canvas.Canvas("ResistorLabels.pdf", pagesize=letter)

    draw_resistor_sticker(c, 0, 0, 9.99999)
    draw_resistor_sticker(c, 0, 1, 0.00055)
    draw_resistor_sticker(c, 0, 2, 0.00551)
    draw_resistor_sticker(c, 1, 0, 0.0552)
    draw_resistor_sticker(c, 1, 1, 0.553)
    draw_resistor_sticker(c, 1, 2, 5.54)
    draw_resistor_sticker(c, 2, 0, 55.9)
    draw_resistor_sticker(c, 2, 1, 555)
    draw_resistor_sticker(c, 2, 2, 5560)
    draw_resistor_sticker(c, 3, 0, 55700)
    draw_resistor_sticker(c, 3, 1, 558000)
    draw_resistor_sticker(c, 3, 2, 5590000)
    draw_resistor_sticker(c, 4, 0, 5500000)

    for y in range(3):
        for x in range(10):
            rect = StickerRect(x, y)
            c.setStrokeColor(black, 0.1)
            c.setLineWidth(0)
            c.roundRect(rect.left, rect.bottom, rect.width, rect.height, rect.corner)
    c.showPage()
    c.save()


if __name__ == "__main__":
    main()
