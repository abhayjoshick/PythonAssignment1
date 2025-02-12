import csv

def print_table(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        data = list(csv.reader(file))

    if not data:
        print("Empty CSV file.")
        return

    col_widths = [max(map(len, col)) for col in zip(*data)]

    def print_border():
        print("+" + "+".join("-" * (w + 2) for w in col_widths) + "+")

    def print_row(row):
        print("|" + "|".join(f" {cell:<{col_widths[i]}} " for i, cell in enumerate(row)) + "|")

    print_border()
    for row in data:
        print_row(row)
        if row == data[0]:  
            print_border()
    print_border()

# Usage Example
print_table('csvData.csv')
