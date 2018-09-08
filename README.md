# Redash-API-Client
Redash API Client written in Python.

## Dependencies
* Python3.6+

## Installation
Install using pip:

    pip install redash-api-client

## Getting Started
```python
from redashAPI.client import RedashAPIClient

# Create Client instance
"""
    :args:
    API_KEY
    REDASH_HOST (optional): 'http://localhost:5000' by default
"""
Redash = RedashAPIClient(API_KEY, REDASH_HOST)
```

### Basic Requests
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
Response: [{"name": "Data Source 1", "pause_reason": null, "syntax": "sql", "paused": false, "view_only": false, "type": "mysql", "id": 1}]
"""

# Get particular Data Source
res = Redash.get('data_sources/1')
res.json()
"""
Response: {"scheduled_queue_name": "scheduled_queries", "name": "Data Source 1", "pause_reason": null, "queue_name": "queries", "syntax": "sql", "paused": false, "options": {"passwd": "--------", "host": "mysql", "db": "mds", "port": 3306, "user": "root"}, "groups": {"2": false}, "type": "mysql", "id": 1}
"""

# Create New Data Source
Redash.post('data_sources', {
    "name": "New Data Source",
    "type": "mysql",
    "options": {
        "dbname": DB_NAME,
        "host": DB_HOST,
        "user": DB_USER,
        "passwd": DB_PASSWORD,
        "port": DB_PORT
    }
})

# Delete Data Source 1
Redash.delete('data_sources/1')
```

### Useful Methods
```python
# Connect to a Data Source
"""
    :args:
    DATA_SOURCE_NAME
    DATA_SOURCE_TYPE: ["sqlite", "mysql", "pg", "mongodb", "mssql" ...]
    OPTIONS
"""
Redash.connect_data_source("First Data Source", "pg", {
    "dbname": DB_NAME,
    "host": DB_HOST,
    "user": DB_USER,
    "passwd": DB_PASSWORD,
    "port": DB_PORT
})


# Create Query
"""
    :args:
    QUERY_NAME
    DATA_SOURCE_ID
    QUERY_STRING
    WITH_RESULT (optional): Generate query_result automatically, True by default
"""
Redash.create_query("First Query", 1, "SELECT * FROM table_name;", False)


# Generate Query Result
"""
    :args:
    DATA_SOURCE_ID
    QUERY_STRING
    QUERY_ID
"""
Redash.generate_query_result(1, "SELECT * FROM table_name;", 1)


# Create Visualization
"""
    :args:
    NAME
    QUERY_ID
    CHART_TYPE: ["line", "column", "area", "pie", "scatter", "bubble", "box"]
    X_AXIS_COLUMN
    Y_AXIS_COLUMN
    Y_LABEL (optional): Custom name for legend
"""
Redash.create_visualization("First Visualization", 1, "line", X_AXIS_COLUMN, Y_AXIS_COLUMN, Y_LABEL)


# Create Dashboard
"""
    :args:
    NAME
"""
Redash.create_dashboard("First Dashboard")


# Add Visualization into Dashboard
"""
    :args:
    DASHBOARD_ID
    VISUALIZATION_ID
    FULL_WIDTH (optional): Full width or not on dashboard, False by default
"""
Redash.add_to_dashboard(1, 1, True)


# Publish Dashboard and get its public URL
"""
    :args:
    DASHBOARD_ID
"""
url = Redash.get_dashboard_public_url(1)
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
