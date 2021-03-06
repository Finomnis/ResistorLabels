#!/usr/bin/env python3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import black, toColor, HexColor, gray

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

        if self.ohms_exp < 0:
            rendered_num = str(self.ohms_val)
            while rendered_num[-1] == "0":
                rendered_num = rendered_num[:-1]
            if self.ohms_exp == -1:
                return "0." + rendered_num
            if self.ohms_exp == -2:
                return "0.0" + rendered_num
            if self.ohms_exp == -3:
                return "0.00" + rendered_num

        return self.get_prefixed_number() + self.get_prefix()


def resistor_color_table(num):
    return [
        HexColor("#000000"),
        HexColor("#994d00"),
        HexColor("#FF0000"),
        HexColor("#FF9900"),
        HexColor("#FFFF00"),
        HexColor("#00FF00"),
        HexColor("#0000FF"),
        HexColor("#FF00FF"),
        HexColor("#CCCCCC"),
        HexColor("#FFFFFF"),
    ][num]


def draw_fancy_resistor_stripe(c, x, y, width, height, color_table):
    c.setFillColor(color_table[2])
    c.rect(x, y+height*5/6, width, height/6, fill=1, stroke=0)
    c.setFillColor(color_table[1])
    c.rect(x, y+height*4/6, width, height/6, fill=1, stroke=0)
    c.setFillColor(color_table[0])
    c.rect(x, y+height*3/6, width, height/6, fill=1, stroke=0)
    c.setFillColor(color_table[1])
    c.rect(x, y+height*2/6, width, height/6, fill=1, stroke=0)
    c.setFillColor(color_table[2])
    c.rect(x, y+height*1/6, width, height/6, fill=1, stroke=0)
    c.setFillColor(color_table[3])
    c.rect(x, y+height*0/6, width, height/6, fill=1, stroke=0)


def draw_resistor_stripe(c, x, y, width, height, stripe_value):

    if 0 <= stripe_value <= 9:
        c.setFillColor(resistor_color_table(stripe_value))
        c.rect(x, y, width, height, fill=1, stroke=0)
        return

    elif stripe_value == -1:
        gold_table = [
            HexColor("#fefefe"),
            HexColor("#f7febe"),
            HexColor("#effe41"),
            HexColor("#c5d24f"),
        ]

        draw_fancy_resistor_stripe(c, x, y, width, height, gold_table)
        return

    elif stripe_value == -2:
        silver_table = [
            HexColor("#fefefe"),
            HexColor("#e0e0e0"),
            HexColor("#cdcdcd"),
            HexColor("#b5b5b5"),
        ]

        draw_fancy_resistor_stripe(c, x, y, width, height, silver_table)
        return

    else:

        c.setLineWidth(0.5)
        c.setFillColor(gray, 0.3)
        c.setStrokeColorRGB(0.5, 0.5, 0.5, 1.0)
        c.rect(x, y, width, height, fill=1, stroke=1)
        c.line(x, y, x + width, y + height)
        c.line(x + width, y, x, y + height)
        return


def draw_resistor_colorcode(c, value, color1, color2, x, y, width, height, num_codes):

    if value.ohms_exp < num_codes - 4:
        return

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

        draw_resistor_stripe(c,
                             x + border + corner + stripe_width / 2 + 2 * stripe_width * i,
                             y + border,
                             stripe_width,
                             height - 2 * border,
                             stripe_value)

    draw_resistor_stripe(c,
                         x + width - border - corner - stripe_width * 1.5,
                         y + border,
                         stripe_width,
                         height - 2 * border,
                         -3)

    c.setFillColor(black)
    c.setStrokeColor(black, 1)
    c.setLineWidth(0.5)
    c.roundRect(x+border, y+border, width-2*border, height-2*border, corner)


def get_3digit_code(value):
    if value.ohms_val % 10 != 0:
        return ""

    digits = str(value.ohms_val // 10)

    if value.ohms_exp > 0:
        multiplier = str(value.ohms_exp - 1)
        return digits + multiplier

    if value.ohms_exp == 0:
        return digits[0] + "R" + digits[1]

    if value.ohms_exp == -1:
        return "R" + digits

    if value.ohms_exp == -2:
        if value.ohms_val % 100 != 0:
            return ""
        return "R0" + digits[0]

    return ""


def get_4digit_code(value):
    digits = str(value.ohms_val)

    if value.ohms_exp > 1:
        multiplier = str(value.ohms_exp - 2)
        return digits + multiplier

    if value.ohms_exp == 1:
        return digits[0] + digits[1] + "R" + digits[2]

    if value.ohms_exp == 0:
        return digits[0] + "R" + digits[1] + digits[2]

    if value.ohms_exp == -1:
        return "R" + digits

    if value.ohms_exp == -2:
        if value.ohms_val % 10 != 0:
            return ""
        return "R0" + digits[0] + digits[1]

    if value.ohms_exp == -3:
        if value.ohms_val % 100 != 0:
            return ""
        return "R00" + digits[0]

    return ""


def get_eia98_code(value):
    eia98_coding_table = {
        100: "01", 178: "25", 316: "49", 562: "73",
        102: "02", 182: "26", 324: "50", 576: "74",
        105: "03", 187: "27", 332: "51", 590: "75",
        107: "04", 191: "28", 340: "52", 604: "76",
        110: "05", 196: "29", 348: "53", 619: "77",
        113: "06", 200: "30", 357: "54", 634: "78",
        115: "07", 205: "31", 365: "55", 649: "79",
        118: "08", 210: "32", 374: "56", 665: "80",
        121: "09", 215: "33", 383: "57", 681: "81",
        124: "10", 221: "34", 392: "58", 698: "82",
        127: "11", 226: "35", 402: "59", 715: "83",
        130: "12", 232: "36", 412: "60", 732: "84",
        133: "13", 237: "37", 422: "61", 750: "85",
        137: "14", 243: "38", 432: "62", 768: "86",
        140: "15", 249: "39", 442: "63", 787: "87",
        143: "16", 255: "40", 453: "64", 806: "88",
        147: "17", 261: "41", 464: "65", 825: "89",
        150: "18", 267: "42", 475: "66", 845: "90",
        154: "19", 274: "43", 487: "67", 866: "91",
        158: "20", 280: "44", 499: "68", 887: "92",
        162: "21", 287: "45", 511: "69", 909: "93",
        165: "22", 294: "46", 523: "70", 931: "94",
        169: "23", 301: "47", 536: "71", 953: "95",
        174: "24", 309: "48", 549: "72", 976: "96",
    }

    if value.ohms_val not in eia98_coding_table:
        return ""

    digits = eia98_coding_table[value.ohms_val]

    multiplier_table = ["Z", "Y", "X", "A", "B", "C", "D", "E", "F"]
    if not (0 <= value.ohms_exp+1 < len(multiplier_table)):
        return ""

    multiplier = multiplier_table[value.ohms_exp+1]

    return digits + multiplier


def draw_resistor_sticker(c, row, column, ohms, draw_center_line=True):
    rect = StickerRect(row, column)

    # Squish horizontally by a bit, to prevent clipping
    rect.width -= 0.1*inch
    rect.left += 0.05*inch

    # Draw middle line
    if draw_center_line:
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
    smd_font_size = 0.08 * inch
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
                            toColor("hsl(55, 54%, 100%)"), toColor("hsl(55, 54%, 70%)"),
                            rect.left + rect.width/2,
                            rect.bottom + rect.height/4 - rect.height/45,
                            rect.width/4, rect.height/4,
                            3)

    draw_resistor_colorcode(c, resistor_value,
                            toColor("hsl(197, 59%, 100%)"), toColor("hsl(197, 59%, 73%)"),
                            rect.left + rect.width * 0.75,
                            rect.bottom + rect.height/4 - rect.height/45,
                            rect.width/4, rect.height/4,
                            4)

    c.setFont('Arial Bold', smd_font_size * 1.35)
    c.drawString(rect.left + rect.width/2 + rect.width/32, rect.bottom + rect.height/13, get_3digit_code(resistor_value))
    c.drawCentredString(rect.left + rect.width*3/4, rect.bottom + rect.height/13, get_4digit_code(resistor_value))
    c.drawRightString(rect.left + rect.width - rect.width/32, rect.bottom + rect.height/13, get_eia98_code(resistor_value))


def render_stickers(c, values, draw_center_line=True):
    for (rowId, row) in enumerate(values):
        for (columnId, value) in enumerate(row):
            if not value:
                continue
            draw_resistor_sticker(c, rowId, columnId, value, draw_center_line)


def render_outlines(c):
    for y in range(3):
        for x in range(10):
            rect = StickerRect(x, y)
            c.setStrokeColor(black, 0.1)
            c.setLineWidth(0)
            c.roundRect(rect.left, rect.bottom, rect.width, rect.height, rect.corner)


def main():

    c = canvas.Canvas("ResistorLabels.pdf", pagesize=letter)

    # #######################################################################
    # Put your own resistor values in here!
    # This has to be a grid of 10*3 values.
    # Add "None" if no label should get generated at a specific position.
    # #######################################################################
    render_stickers(c, [
        [          .1,          .02,         .003 ],
        [           1,           12,           13 ],
        [         210,          220,          330 ],
        [        3100,         3200,         3300 ],
        [       41000,        42000,        43000 ],
        [      510000,         None,       530000 ],
        [     6100000,      6200000,      6300000 ],
        [    71000000,     72000000,     73000000 ],
        [   810000000,    820000000,    830000000 ],
        [  9100000000,   9200000000,   3300000000 ],
    ])

    ## Add this if you want to see the outlines of the labels.
    ## Recommended to be commented out for the actual printing.
    # render_outlines(c)

    c.showPage()
    c.save()


if __name__ == "__main__":
    main()
