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
Response: [{"name": "Data Source 1", "pause_reason": null, "syntax": "sql", "paused": false, "view_only": false, "type": "mysql", "id": 1}]
"""

# Get specific Data Source
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

# Delete Data Source
Redash.delete('data_sources/1')
```

### Methods
```python
# Create Data Source
"""
    :args:
    DATA_SOURCE_TYPE: ["sqlite", "mysql", "pg", "mongodb", "mssql" ...]
    DATA_SOURCE_NAME
    OPTIONS
"""
Redash.create_data_source("pg", "First Data Source", {
    "dbname": DB_NAME,
    "host": DB_HOST,
    "user": DB_USER,
    "passwd": DB_PASSWORD,
    "port": DB_PORT
})


# Create Query
"""
    :args:
    DATA_SOURCE_ID
    QUERY_NAME
    QUERY_STRING
    DESC (optional)
    WITH_RESULTS (optional): Generate query results automatically, True by default
"""
Redash.create_query(1, "First Query", "SELECT * FROM table_name;", with_results=False)


# Refresh Query
"""
    :args:
    QUERY_ID
"""
Redash.refresh_query(1)


# Generate Query Result
"""
    :args:
    QUERY_ID
"""
Redash.generate_query_result(1)


# Create Visualization
"""
    :args:
    QUERY_ID
    CHART_TYPE: ["table", "line", "column", "area", "pie", "scatter", "bubble", "box", "pivot"]
    CHART_NAME
    COLUMNS (optional): Columns for Table (Required if CHART_TYPE is table)
    X_AXIS (optional): Column for X Axis (Required if CHART_TYPE is not table nor pivot)
    Y_AXIS (optional): Columns for Y Axis (Required if CHART_TYPE is not table nor pivot)
    CUSTOM_OPTIONS (optional): Custom options for Visualization
    DESC (optional)
"""
Redash.create_visualization(1, "table", "First Visualization", columns=[{"name": "column1", "type": "string"}, {"name": "column2", "type": "datetime"}])
Redash.create_visualization(1, "line", "Second Visualization", x_axis="column1", y_axis=[{"type": "line", "name": "column2", "label": "c2"}])


# Create Dashboard
"""
    :args:
    NAME
"""
Redash.create_dashboard("First Dashboard")


# Add Widget into Dashboard
"""
    :args:
    DASHBOARD_ID
    TEXT (optional)
    VISUALIZATION_ID (optional)
    FULL_WIDTH (optional): Full width or not on dashboard, False by default
    POSITION (optional)
"""
Redash.add_widget(1, text="Test")
Redash.add_widget(1, visualization_id=1, full_width=True)


# Publish Dashboard
"""
    :args:
    DASHBOARD_ID
"""
url = Redash.publish_dashboard(1)
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
