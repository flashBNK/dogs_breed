import time

from django.db import connection, reset_queries


def speed_queryset(queryset):
    reset_queries()

    start = time.perf_counter()

    result = list(queryset)

    elapsed = (time.perf_counter() - start) * 1000

    print("=" * 100)
    print(f"SQL-запросов: {len(connection.queries)}")
    print(f"Время: {elapsed:.2f} ms")
    print()

    for i, query in enumerate(connection.queries, start=1):
        print(f"Запрос №{i}")
        print(f"SQL time: {query['time']} sec")
        print(query["sql"])
        print("-" * 100)

    return result