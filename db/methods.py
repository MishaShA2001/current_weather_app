"""Methods to use database to save request history"""
from typing import Any, Optional, Iterator, Callable
import sqlite3
from contextlib import contextmanager
from db.config import DB_FILE_NAME
from db.sql_templates import (CREATE_TABLE_QUERY, INSERT_INTO_QUERY,
                              SELECT_FROM_QUERY, ORDER_TEMPLATE,
                              LIMIT_TEMPLATE, DELETE_FROM_QUERY)
from utils.errors import (DatabaseProblemError, errors_handler)


@contextmanager
def open_db(db_file_name: str) -> Optional[Iterator[sqlite3.Cursor]]:
    try:
        connection = sqlite3.connect(db_file_name)
        cursor = connection.cursor()
        yield cursor
        connection.commit()
        connection.close()
    except sqlite3.Error:
        raise DatabaseProblemError


def db_connect(func: Callable[..., None]) -> Callable[..., None]:
    """Database connect decorator

    :param func: function to decorate
    :return: decorated function
    """

    def wrapper(*args, **kwargs) -> None:
        with open_db(DB_FILE_NAME) as cursor:
            func(*args, **kwargs, cursor=cursor)

    return wrapper


@errors_handler
@db_connect
def initialize_db_table(table_name: str, table_columns: dict[str, str],
                        **kwargs) -> None:
    """Creates connection and table if it's necessary

    :param table_name: table to be initialized
    :param table_columns: columns in format 'column_name: column_type'
    :param kwargs: for getting cursor through the decorator
    """
    table_columns = ', '.join(
        [f'{key} {value}' for key, value in table_columns.items()])

    kwargs['cursor'].execute(CREATE_TABLE_QUERY.format(
        table_name=table_name,
        table_columns=table_columns
    ))


@db_connect
def insert_into_table(table_name: str, table_columns: dict[str, str],
                      values: dict[str, Any], **kwargs) -> None:
    """Inserts some raw into the table

    :param table_name: to insert into
    :param table_columns: columns in format 'column_name: column_type'
    :param values: values in format 'column_name: value'
    :param kwargs: for getting cursor through the decorator
    """
    values = ', '.join(
        [f"'{value}'" if table_columns[key] == 'TEXT' else f'{value}'
         for key, value in values.items()])
    table_columns = ', '.join([f'{key}' for key in table_columns.keys()])

    kwargs['cursor'].execute(INSERT_INTO_QUERY.format(
        table_name=table_name,
        table_columns=table_columns,
        values=values
    ))


def select_from_table(table_name: str, table_columns: dict[str, str],
                      number: str, **kwargs) -> list[tuple[Any, ...]]:
    """Takes all values of some columns from table

    :param table_name: to take values
    :param table_columns: values of which columns to take
    :param number: number of top rows to select (str to insert into template)
    :param kwargs: for order (dict with column and order type)
    :return: rows as a result of query
    """
    table_columns = ', '.join([f'{key}' for key in table_columns.keys()])
    sql_query = SELECT_FROM_QUERY.format(
        table_columns=table_columns, table_name=table_name
    )

    if 'order' in kwargs.keys():
        sql_query += ORDER_TEMPLATE.format(
            table_column=kwargs['order']['table_column'],
            order_type=kwargs['order']['order_type']
        )

    sql_query += LIMIT_TEMPLATE.format(number=number)

    with open_db(DB_FILE_NAME) as cursor:
        return cursor.execute(sql_query).fetchall()


@db_connect
def truncate_table(table_name: str, **kwargs) -> None:
    """Truncates table

    :param table_name: table to truncate
    :param kwargs: for getting cursor through the decorator (cursor)
    """
    kwargs['cursor'].execute(DELETE_FROM_QUERY.format(table_name=table_name))
