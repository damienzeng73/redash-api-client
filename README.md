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
```

### Basic Requests
| URI                | Supported Methods             |
| ------------------ | ----------------------------- |
| *users*            | **GET**, **POST**             |
| *users/1*          | **GET**, **POST**, **DELETE** |
| *data_sources*     | **GET**, **POST**             |
| *data_sources/1*   | **GET**, **POST**, **DELETE** |
| *queries*          | **GET**, **POST**             |
| *queries/1*        | **GET**, **POST**, **DELETE** |
| *query_results*    | **POST**                      |
| *query_results/1*  | **GET**, **POST**, **DELETE** |
| *visualizations*   | **POST**                      |
| *visualizations/1* | **POST**, **DELETE**          |
| *dashboards*       | **GET**, **POST**             |
| *dashboards/slug*  | **GET**, **POST**, **DELETE** |
| *widgets*          | **POST**                      |
| *widgets/1*        | **POST**, **DELETE**          |

Example:
```python
# List all Users
res = Redash.get('users')
res.json()
"""
[{"auth_type": "password", "disabled_at": null, "name": "admin", "groups": [1, 2], "updated_at": "2018-09-08T07:54:03.045582+00:00", "created_at": "2018-09-08T07:54:03.045582+00:00", "is_disabled": false, "id": 1, "profile_image_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=40&d=identicon", "email": "admin@example.com"}]
"""

# Get particular User
res = Redash.get('users/1')
res.json()
"""
{"auth_type": "password", "is_disabled": false, "updated_at": "2018-09-08T07:54:03.045582+00:00", "profile_image_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=40&d=identicon", "disabled_at": null, "groups": [1, 2], "id": 1, "name": "admin", "created_at": "2018-09-08T07:54:03.045582+00:00", "api_key": "5y9ShL6b6haKFdmkDOHPtc4jFnCK5YknFc4mH70k", "email": "admin@example.com"}
"""

# Create User
Redash.post('users', {"name": "New User", "email": "test@example.com"})
```

### Useful Methods
```python
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
