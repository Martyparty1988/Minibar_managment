import csv
from datetime import datetime

def export_csv(data):
    filename = f"analytics_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    filepath = f"./exports/{filename}"
    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    return filepath