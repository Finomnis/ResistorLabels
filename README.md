# ResistorLabels

This script generates labels for resistor zip bags.

It is meant for AVERY 5260 or AVERY L7157 labels and 7x10cm (3"x4") zip bags.

The generated labels include:

-   Resistor value
-   4- and 5-band color codes
-   3- and 4-digit smd codes
-   EIA-96 smd code

<img src="Example.svg">

# Usage

-   Install python3
-   Install the python3 library `reportlab`. This library is used to do the actual PDF generation.
-   Add your own required resistor values in `main()` of `LabelGenerator.py`.
-   If using Avery L7157, change the `layout` value in `main()` to `AVERY_L7157`.
-   Run the script `LabelGenerator.py`!

It will now generate a `ResistorLabels.pdf` that can be used to print onto AVERY 5260/L7157.

# Alternative Font

The default font is 'Arial Bold'. You can alternatively use 'Roboto Bold' by invoking the script with the `--roboto` flag.

'Roboto' is an [open font by google](https://fonts.google.com/specimen/Roboto) and is included in this repository.

Adding the `--roboto` flag is required for Mac OS, as the script currently does not support 'Arial Bold' on Mac OS.

# More Details

This is based on an idea from Zach Poff.

For more details on how to use these labels, visit his website:

https://www.zachpoff.com/resources/quick-easy-and-cheap-resistor-storage/
