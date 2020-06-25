# Redash-API-Client

[![PyPI version fury.io](https://badge.fury.io/py/redash-api-client.svg)](https://pypi.org/project/redash-api-client/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/redash-api-client.svg)](https://pypi.python.org/pypi/redash-api-client/)
[![PyPI license](https://img.shields.io/pypi/l/redash-api-client.svg)](https://pypi.python.org/pypi/redash-api-client/)
[![Downloads](https://pepy.tech/badge/redash-api-client)](https://pepy.tech/project/redash-api-client)

Redash API Client written in Python.

## Dependencies

* Python3.6+

## Installation

    pip install redash-api-client

## Getting Started

```python
from redashAPI import RedashAPIClient

# Create API client instance
"""
    :args:
    API_KEY
    REDASH_HOST (optional): `http://localhost:5000` by default
"""
Redash = RedashAPIClient(API_KEY, REDASH_HOST)
```

### Redash's RESTful API

| URI                | Supported Methods             |
| ------------------ | ----------------------------- |
| *users*            | **GET**, **POST**             |
| *users/1*          | **GET**, **POST**             |
| *data_sources*     | **GET**, **POST**             |
| *data_sources/1*   | **GET**, **POST**, **DELETE** |
| *queries*          | **GET**, **POST**             |
| *queries/1*        | **GET**, **POST**, **DELETE** |
| *query_results*    | **POST**                      |
| *query_results/1*  | **GET**                       |
| *visualizations*   | **POST**                      |
| *visualizations/1* | **POST**, **DELETE**          |
| *dashboards*       | **GET**, **POST**             |
| *dashboards/slug*  | **GET**, **POST**, **DELETE** |
| *widgets*          | **POST**                      |
| *widgets/1*        | **POST**, **DELETE**          |

```python
### EXAMPLE ###

# List all Data Sources
res = Redash.get('data_sources')
res.json()
"""
[
    {
        'name': 'data_source1',
        'pause_reason': None,
        'syntax': 'sql',
        'paused': 0,
        'view_only': False,
        'type': 'pg',
        'id': 1
    },
    ...
]
"""

# Retrieve specific Data Source
res = Redash.get('data_sources/1')
res.json()
"""
{
    "scheduled_queue_name": "scheduled_queries",
    "name": "test1",
    "pause_reason": "None",
    "queue_name": "queries",
    "syntax": "sql",
    "paused": 0,
    "options": {
        "password": "--------",
        "dbname": "bi",
        "user": ""
    },
    "groups": {
        "1":False
    },
    "type": "pg",
    "id": 1
}
"""

# Create New Data Source
Redash.post('data_sources', {
    "name": "New Data Source",
    "type": "pg",
    "options": {
        "dbname": DB_NAME,
        "host": DB_HOST,
        "user": DB_USER,
        "passwd": DB_PASSWORD,
        "port": DB_PORT
    }
})
"""
{
    "scheduled_queue_name": "scheduled_queries",
    "name": "New Data Source",
    "pause_reason": "None",
    "queue_name": "queries",
    "syntax": "sql",
    "paused": 0,
    "options": {
        "dbname": DB_NAME,
        "host": DB_HOST,
        "user": DB_USER,
        "passwd": DB_PASSWORD,
        "port": DB_PORT
    },
    "groups": {
        "2": False
    },
    "type": "pg",
    "id": 2
}
"""

# Delete specific Data Source
Redash.delete('data_sources/2')
```

### Create Data Source

- **_type**

    - Type of Data Source. ([Supported types](https://github.com/getredash/redash/blob/ddb0ef15c1340e7de627e928f80486dfd3d6e1d5/redash/settings/__init__.py#L309-L358))

- **name**

    - Name for Data Source.

- **options**

    - Configuration.

```python
### EXAMPLE ###

Redash.create_data_source("pg", "First Data Source", {
    "dbname": DB_NAME,
    "host": DB_HOST,
    "user": DB_USER,
    "passwd": DB_PASSWORD,
    "port": DB_PORT
})
```

### Create Query

- **ds_id**

    - Data Source ID.

- **name**

    - Name for query.

- **qry**

    - Query string.

- **desc (optional)**

    - Description.

- **with_results (optional)**

    - Generate query results automatically, `True` by default.

- **options (optional)**

    - Custom options.

- **schedule (optional)**

    - Schedule configurations

```python
### EXAMPLE ###

Redash.create_query(1, "First Query", "SELECT * FROM table_name;")
```

### Refresh Query

- **qry_id**

    - Query ID.

```python
### EXAMPLE ###

Redash.refresh_query(1)
```

### Generate Query Result

- **ds_id**

    - Data Source ID.

- **qry**

    - Query String.

- **qry_id (optional)**

    - Query ID.

- **max_age (optional)**

    - If query results less than *max_age* seconds old are available,
    return them, otherwise execute the query; if omitted or -1, returns
    any cached result, or executes if not available. Set to zero to
    always execute.

- **parameters (optional)**

    - A set of parameter values to apply to the query.

- **return_results (optional)**

    - Return results if query is executed successfully, `True` by default.

```python
### EXAMPLE ###

Redash.generate_query_results(1)
```

### Query and Wait Result

- **ds_id**

    - Data Source ID.

- **qry**

    - Query String.

- **timeout (optional)**
    - Defines the time in seconds to wait before cutting the request.

```python
### EXAMPLE ###

Redash.query_and_wait_result(1, 'select * from my_table;', 60)
```

### Create Visualization

- **qry_id**

    - Query ID.

- **_type**

    - Type of Visualization. (`table`, `line`, `column`, `area`, `pie`, `scatter`, `bubble`, `box`, `pivot`)

- **name**

    - Name for Visualization.

- **columns (optional)**

    - Columns for Table. (Required if *_type* is `table`)

- **x_axis (optional)**

    - Column for X Axis. (Required if *_type* is not `table` nor `pivot`)

- **y_axis (optional)**

    - Columns for Y Axis (Required if *_type* is not `table` nor `pivot`)

- **size_column (optional)**

    - Column for size. (Bubble)

- **group_by (optional)**

    - Group by specific column.

- **custom_options (optional)**

    - Custom options for Visualization.

- **desc (optional)**

    - Description.

```python
### EXAMPLE 1 ###

Redash.create_visualization(1, "table", "First Visualization", columns=[
    {"name": "column1", "type": "string"},
    {"name": "column2", "type": "datetime"}
])

### EXAMPLE 2 ###
Redash.create_visualization(1, "line", "Second Visualization", x_axis="column1", y_axis=[
    {"type": "line", "name": "column2", "label": "c2"}
])
```

### Create Dashboard

- **name**

    - Name for Dashboard.

```python
### EXAMPLE ###

Redash.create_dashboard("First Dashboard")
```

### Add Widget into Dashboard

- **db_id**

    - Dashboard ID.

- **text (optional)**

    - Text Widget.

- **vs_id (optional)**

    - Visualization ID.

- **full_width (optional)**

    - Full width or not, `False` by default.

- **position (optional)**

    - Custom position for Widget.

```python
### EXAMPLE 1 ###

Redash.add_widget(1, text="Test")

### EXAMPLE 2 ###
Redash.add_widget(1, visualization_id=1, full_width=True)
```

### Publish Dashboard

- **db_id**

    - Dashboard ID.

```python
### EXAMPLE ###

url = Redash.publish_dashboard(1)
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
