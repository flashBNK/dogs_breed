import logging
import time

from django.db import connection, reset_queries

logger = logging.getLogger(__name__)


def speed_queryset(queryset):
    reset_queries()

    start = time.perf_counter()

    result = list(queryset)

    elapsed = (time.perf_counter() - start) * 1000

    logger.debug("SQL-запросов: %s", len(connection.queries))
    logger.debug("Время: %s ms", elapsed)

    for i, query in enumerate(connection.queries, start=1):
        logger.debug("Запрос № %s", i)
        logger.debug("SQL time: %s sec", query["time"])
        logger.debug(query["sql"])

    return result
