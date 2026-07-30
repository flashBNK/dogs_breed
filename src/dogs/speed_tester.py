import logging
import time

from django.db import connection, reset_queries

logger = logging.getLogger(__name__)


def speed_queryset(queryset):
    reset_queries()

    start = time.perf_counter()

    result = list(queryset)

    elapsed = (time.perf_counter() - start) * 1000

    logger.info("SQL-запросов: %s", len(connection.queries))
    logger.info("Время: %s ms", elapsed)

    for i, query in enumerate(connection.queries, start=1):
        logger.info("Запрос № %s", i)
        logger.info("SQL time: %s sec", query["time"])
        logger.info(query["sql"])

    return result
