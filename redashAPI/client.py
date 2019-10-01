import json
import requests

class RedashAPIClient(object):
    def __init__(self, api_key, host='http://localhost:5000'):
        self.api_key = api_key
        self.host = host

        self.s = requests.Session()
        self.s.headers.update({"Authorization": f"Key {api_key}"})

    def get(self, uri):
        res = self.s.get(f"{self.host}/api/{uri}")

        if res.status_code != 200:
            raise Exception(f"Retrieve data from URL: /api/{uri} failed.")

        return res

    def post(self, uri, payload=dict()):
        data = json.dumps(payload)

        self.s.headers.update({"Content-Type": "application/json"})
        res = self.s.post(f"{self.host}/api/{uri}", data=data)

        if res.status_code != 200:
            raise Exception(f"Post data to URL: /api/{uri} failed.")

        return res

    def delete(self, uri):
        res = self.s.delete(f"{self.host}/api/{uri}")

        if res.status_code != 200:
            raise Exception(f"Delete data from URL: /api/{uri} failed.")

        return res

    def create_data_source(self, _type, name, options):
        payload = {
            "type": _type,
            "name": name,
            "options": options
        }

        return self.post('data_sources', payload)

    def create_query(self, ds_id, name, qry, desc="", with_results=True):
        payload = {
            "data_source_id": ds_id,
            "name": name,
            "query": qry,
            "description": desc
        }

        res = self.post('queries', payload)
        qry_id = res.json().get('id', None)

        if with_results:
            if qry_id is None:
                raise Exception("Failed to create query.")

            return self.generate_query_results(qry_id)
        return res

    def refresh_query(self, qry_id):
        return self.post(f"queries/{qry_id}/refresh")

    def generate_query_results(self, qry_id):
        res = self.get('queries')
        results = res.json().get('results', [])

        ds_id, qry = next(((q['data_source_id'], q['query']) for q in results if q['id'] == qry_id), (None, None))

        if ds_id is None or qry is None:
            raise Exception("Query not found.")

        payload = {
            "data_source_id": ds_id,
            "query_id": qry_id,
            "query": qry
        }

        return self.post('query_results', payload)

    def create_visualization(self, qry_id, _type, name, x_axis=None, y_axis=None, y_label=None, table_columns=None, pivot_table_options=None, desc=None):
        if _type == 'table':
            chart_type = 'TABLE'
            options = {
                "autoHeight": True,
                "defaultColumns": 3,
                "defaultRows": 15,
                "itemsPerPage": 10,
                "minColumns": 1,
                "columns": table_columns
            }

        elif _type == 'pivot':
            chart_type = 'PIVOT'
            options = pivot_table_options

        else:
            chart_type = 'CHART'
            options = {
                "globalSeriesType": _type,
                "sortX": True,
                "legend": {"enabled": True},
                "yAxis": [{"type": "linear"}, {"type": "linear", "opposite": True}],
                "xAxis": {"type": "category", "labels": {"enabled": True}},
                "error_y": {"type": "data", "visible": True},
                "series": {"stacking": None, "error_y": {"type": "data", "visible": True}},
                "seriesOptions": {
                    y_axis: {
                        "zIndex": 0,
                        "index": 0,
                        "type": _type,
                        "name": y_label or y_axis,
                        "yAxis": 0
                    }
                },
                "columnMapping": {
                    x_axis: "x",
                    y_axis: "y"
                },
                "showDataLabels": True if _type == 'pie' else False
            }

        payload = {
            "name": name,
            "type": chart_type,
            "query_id": qry_id,
            "description": desc,
            "options": options
        }

        return self.post('visualizations', payload)

    def create_dashboard(self, name):
        payload = {
            "name": name
        }

        return self.post('dashboards', payload)

    def add_to_dashboard(self, db_id, vs_id, full_width=False, position=None):
        res = self.get(f"dashboards")

        results = res.json().get('results', [])
        slug = next((d['slug'] for d in results if d['id'] == db_id), None)

        if slug is None:
            raise Exception("Dashboard not found.")

        payload = {
            "dashboard_id": db_id,
            "visualization_id": vs_id,
            "width": 1,
            "options": {
                "position": position or self.calculate_widget_position(slug, full_width)
            }
        }

        return self.post('widgets', payload)

    def calculate_widget_position(self, slug, full_width):
        position = {
            "col": 0,
            "row": 0,
            "sizeX": 3,
            "sizeY": 8
        }

        res = self.get(f'dashboards/{slug}')
        widgets = res.json().get('widgets', None)

        full_width_widgets_count = 0
        for w in widgets:
            if w['options']['position']['sizeX'] == 6:
                full_width_widgets_count += 1

        if len(widgets) > 0:
            row, col = divmod(len(widgets) - full_width_widgets_count, 2)

            position['row'] = (row + full_width_widgets_count) * 8
            position['col'] = col * 3

        if full_width:
            position['sizeX'] = 6

        return position

    def publish_dashboard(self, db_id):
        try:
            self.post(f"dashboards/{db_id}", {"is_draft": False})
        except Exception as e:
            raise e

        res = self.post(f"dashboards/{db_id}/share")
        public_url = res.json().get('public_url', None)

        return public_url
