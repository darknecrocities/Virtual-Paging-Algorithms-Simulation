import random

def generate_random_string(length, max_page=9):
    return [random.randint(0, max_page) for _ in range(length)]

def generate_locality_string(length, max_page=9):
    # Simulate temporal/spatial locality
    # We pick a subset of pages and repeat them heavily
    if length == 0:
        return []
    pages = []
    current_locality = [random.randint(0, max_page) for _ in range(min(3, max_page+1))]
    for _ in range(length):
        if random.random() < 0.8: # 80% chance to use a page in current locality
            pages.append(random.choice(current_locality))
        else: # 20% explore new page and add to locality
            new_page = random.randint(0, max_page)
            pages.append(new_page)
            if current_locality:
                current_locality.pop(0)
            current_locality.append(new_page)
    return pages

def generate_worst_case_string(num_frames, length):
    # For LRU/FIFO, worst case is cycling through (num_frames + 1) pages
    # e.g. frames=3 -> sequence: 0, 1, 2, 3, 0, 1, 2, 3
    pages = []
    cycle_size = num_frames + 1
    for i in range(length):
        pages.append(i % cycle_size)
    return pages
