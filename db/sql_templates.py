"""Templates for SQL queries (basic)"""
CREATE_TABLE_QUERY = ('CREATE TABLE IF NOT EXISTS '
                      '{table_name} ({table_columns})')
INSERT_INTO_QUERY = ('INSERT INTO {table_name} ({table_columns}) '
                     'VALUES ({values})')
SELECT_FROM_QUERY = 'SELECT {table_columns} FROM {table_name}'
ORDER_TEMPLATE = ' ORDER BY {table_column} {order_type}'
LIMIT_TEMPLATE = ' LIMIT {number}'
DELETE_FROM_QUERY = 'DELETE FROM {table_name}'
