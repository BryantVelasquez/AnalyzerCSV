import csv

def load_csv(path):
    try:
        with open(path, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader]
    except FileNotFoundError:
        print(f"Error: File not found at '{path}'.")
        return []
    except Exception as e:
        print(f"Error reading '{path}': {e}")
        return []

def extract_amounts(records):

    amounts = []
    for record in records:
        sub = record.get('Amount_Subtracted', '').strip()
        add = record.get('Amount_Added',     '').strip()

        if sub:
            try:
                num = float(sub.replace(',', ''))
            except ValueError:
                print(f"Warning: can’t parse debit '{sub}'")
                continue
            num = -num

        elif add:
            try:
                num = float(add.replace(',', ''))
            except ValueError:
                print(f"Warning: can’t parse credit '{add}'")
                continue
        else:
            # neither debit nor credit
            continue

        amounts.append(num)
    return amounts

def compute_stats(amounts):
    """
    Given a list of floats, return a dict with
    count, total, and average.
    """
    count = len(amounts)
    total = sum(amounts)
    average = total / count if count else 0
    return {
        'count': count,
        'total': total,
        'average': average
    }

def display_stats(stats):
   
    print(f"Number of records:  {stats['count']}")
    print(f"Total amount     : ${stats['total']:,.2f}")
    print(f"Average amount   : ${stats['average']:,.2f}")

if __name__ == "__main__":
    path = input("Enter CSV path: ")
    records = load_csv(path)
    if not records:
        print("No records loaded. Exiting.")
        exit()

    amounts = extract_amounts(records)
    if not amounts:
        print("No valid amounts found. Exiting.")
        exit()

    stats = compute_stats(amounts)
    display_stats(stats)
