@staticmethod
def to_csv(obj: dict, output_name: str) -> None:
    import csv
    try:
        with open(output_name, 'w', newline='', encoding='utf-8') as csvfile:

            if isinstance(obj, dict):
                writer = csv.DictWriter(csvfile, fieldnames=list(obj.keys()))

                writer.writeheader()
                writer.writerows(obj)

    except Exception:
        import traceback

        traceback.print_exc()
