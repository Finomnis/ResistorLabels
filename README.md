# ResistorLabels

This script generates labels for resistor zip bags.

It is meant for AVERY 5260 or AVERY L7157 labels and 7x10cm (3"x4") zip bags.

The generated labels include:

-   Resistor value
-   4- and 5-band color codes
-   3- and 4-digit smd codes
-   EIA-96 smd code

<img src="images\Example.svg">

# Usage

-   Install python3
-   Install the python3 library `reportlab`. This library is used to do the actual PDF generation.
-   Add your own required resistor values in `main()` of `LabelGenerator.py`.
-   If using Avery L7157, change the `layout` value in `main()` to `AVERY_L7157`.
-   Run the script `LabelGenerator.py`!

It will now generate a `ResistorLabels.pdf` that can be used to print onto AVERY 5260/L7157.

For all the non-programmers, there are also pre-generated versions with all
common resistor values for [Avery 5260](./CommonValuesAvery5260.pdf) and [Avery L7157](./CommonValuesAveryL7157.pdf).


# More Details

This is based on an idea from Zach Poff.

For more details on how to use these labels, visit his website:

https://www.zachpoff.com/resources/quick-easy-and-cheap-resistor-storage/

# Modifications

Here are some community modifications/improvements of this project:
- [securelyfitz](https://github.com/securelyfitz/ResistorLabels): Optimized layout for efficiency <br>
  [<img src="https://github.com/securelyfitz/ResistorLabels/blob/5e4db032fd8469aa25ab555384a5f132b6b08443/Example.png" width=400>](https://github.com/securelyfitz/ResistorLabels)
- [prochazkaml](https://github.com/prochazkaml/ComponentLabels): Support for other types of components <br>
  [<img src="https://github.com/user-attachments/assets/97d1cfc7-5ef2-4d29-b490-5f422465625b" width=400>](https://github.com/prochazkaml/ComponentLabels)
