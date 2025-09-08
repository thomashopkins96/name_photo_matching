@staticmethod
def to_csv(obj, output_name: str) -> None:
    import csv
    try:
        with open(output_name, 'w', newline='', encoding='utf-8') as csvfile:
            # Case 1: list of dicts
            if isinstance(obj, list) and obj and isinstance(obj[0], dict):
                writer = csv.DictWriter(csvfile, fieldnames=list(obj[0].keys()))
                writer.writeheader()
                writer.writerows(obj)

            # Case 2: dict of lists
            elif isinstance(obj, dict) and all(isinstance(v, list) for v in obj.values()):
                fieldnames = list(obj.keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                # transpose rows: zip values together
                for row in zip(*obj.values()):
                    writer.writerow(dict(zip(fieldnames, row)))

            # Case 3: single dict (write one row)
            elif isinstance(obj, dict):
                writer = csv.DictWriter(csvfile, fieldnames=list(obj.keys()))
                writer.writeheader()
                writer.writerow(obj)

            else:
                raise ValueError("Unsupported data structure for CSV export.")

    except Exception:
        import traceback
        traceback.print_exc()
