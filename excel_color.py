import openpyxl
from openpyxl.styles import PatternFill

# Create a new workbook and select the active worksheet
workbook = openpyxl.Workbook()
sheet = workbook.active

# Add some data to the worksheet
data = [
    ["Name", "Age", "Grade"],
    ["Alice", 24, "A"],
    ["Bob", 22, "B"],
    ["Charlie", 23, "C"]
]

for row in data:
    sheet.append(row)

# Define some colors
red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")
green_fill = PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")
blue_fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")

# Apply color to specific cells
sheet["A1"].fill = red_fill  # Color the header cell A1 red
sheet["B2"].fill = green_fill  # Color the cell B2 green
sheet["C3"].fill = blue_fill  # Color the cell C3 blue

# Save the workbook
workbook.save("colored_cells.xlsx")
