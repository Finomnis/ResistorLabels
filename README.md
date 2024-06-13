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


# Troubleshooting

If the label comes out misaligned like this: [<a href="images\misaligned.jpg"><img src="images\misaligned.jpg" width="100"></a>](misaligned.jpg), follow these steps to troubleshoot:

- **Check the Printer Driver:**
  - Go to "Settings" and select the printer in question (e.g., Brother HL-L3230CDW).
  - Click on "Printer Properties": [<a href="images\001.png"><img src="images\001.png" width="50"></a>](001.png)
  - In the "Printer Properties" window, check the "Driver".
  - If it says "Microsoft IPP Class Driver" [<a href="images\002.png"><img src="images\002.png" width="50"></a>](002.png), this will cause misalignment issues when printing labels.

- **Update the Vendor's Driver:**
  - Go to the vendor's website to download and install the actual printer driver.
  - Return to "Printer Properties" and select the vendor's driver like so: [<a href="images\003.png"><img src="images\003.png" width="50"></a>](003.png)

- **Print with Proper Settings:**
  - Avery recommends using Adobe PDF Reader to print the labels.
  - Before printing, make sure "Actual size" is selected.
  - Then click on "Properties" next to the printer: [<a href="images\005.png"><img src="images\005.png" width="50"></a>](005.png)
  - This will bring up a new window. Ensure the Media Type is set to "Label": [<a href="images\004.png"><img src="images\004.png" width="50"></a>](004.png)
  - Click "OK" and exit the Printer Properties window.
  - Click "Print" to continue.

Note: Some printers may require manually feeding the label, where the label must be pushed in until the printer's roller is engaged. Follow the manufacturer's [instructions](https://support.brother.com/g/b/faqendbranchprintable.aspx?c=gb&lang=en&pro


# More Details

This is based on an idea from Zach Poff.

For more details on how to use these labels, visit his website:

https://www.zachpoff.com/resources/quick-easy-and-cheap-resistor-storage/
