import csv

def write_results(entries: list, output_path: str):
    with open(output_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ip", "status_code"])

        for entry in entries:
            writer.writerow([entry.ip, entry.status_code])