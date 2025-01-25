import random
import timeit
from collections import OrderedDict, Counter

# Визначимо глобальні змінні
ARRAY_SIZE = 100_000
QUERY_COUNT = 50_000
CACHE_SIZE = 1000

# Генеруємо випадковий масив
array = [random.randint(1, 100) for _ in range(ARRAY_SIZE)]

# Генеруємо випадкові запити
queries = []
for _ in range(QUERY_COUNT):
    if random.choice(['Range', 'Update']) == 'Range':
        L = random.randint(0, ARRAY_SIZE - 1)
        R = random.randint(L, ARRAY_SIZE - 1)
        queries.append(('Range', L, R))
    else:
        index = random.randint(0, ARRAY_SIZE - 1)
        value = random.randint(1, 100)
        queries.append(('Update', index, value))

# Функції без кешування
def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])

def update_no_cache(array, index, value):
    array[index] = value

# Реалізація LRU-кешу
class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

# Ініціалізація кешу
cache = LRUCache(CACHE_SIZE)

def range_sum_with_cache(array, L, R):
    key = (L, R)
    cached_result = cache.get(key)
    if cached_result != -1:
        return cached_result
    
    result = sum(array[L:R+1])
    cache.put(key, result)
    return result

def update_with_cache(array, index, value):
    array[index] = value
    cache.cache.clear()  # Очищаємо кеш після оновлення

# Функції для вимірювання часу
def time_no_cache():
    for query in queries:
        if query[0] == 'Range':
            range_sum_no_cache(array, query[1], query[2])
        else:
            update_no_cache(array, query[1], query[2])

def time_with_cache():
    for query in queries:
        if query[0] == 'Range':
            range_sum_with_cache(array, query[1], query[2])
        else:
            update_with_cache(array, query[1], query[2])

# Вимірювання часу без кешування
no_cache_time = timeit.timeit(time_no_cache, number=1)

# Вимірювання часу з кешуванням
with_cache_time = timeit.timeit(time_with_cache, number=1)

# Підрахунок кількості однакових запитів
query_counter = Counter(queries)
duplicate_queries = {query: count for query, count in query_counter.items() if count > 1}

print(f'Час виконання без кешування: {no_cache_time:.2f} секунд')
print(f'Час виконання з LRU-кешем: {with_cache_time:.2f} секунд')
print(f'Кількість однакових запитів: {len(duplicate_queries)}')