import json
import requests

class RedashAPIClient(object):
    def __init__(self, api_key, host='http://localhost:5000'):
        self.host = host
        self.api_key = api_key

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

    def connect_data_source(self, name, _type, options):
        payload = {
            "name": name,
            "type": _type,
            "options": options
        }

        return self.post('data_sources', payload)

    def create_query(self, name, ds_id, qry, desc="", with_result=True):
        payload = {
            "name": name,
            "data_source_id": ds_id,
            "query": qry,
            "description": desc
        }

        if with_result:
            try:
                res = self.post('queries', payload)
                qry_id = res.json()['id']
            except Exception as e:
                raise e

            return self.generate_query_result(ds_id, qry, qry_id)
        return self.post('queries', payload)

    def generate_query_result(self, ds_id, qry, qry_id):
        payload = {
            "data_source_id": ds_id,
            "query": qry,
            "query_id": qry_id
        }

        return self.post('query_results', payload)

    def create_visualization(self, name, qry_id, _type, x_axis, y_axis, y_label=None):
        payload = {
            "name": name,
            "type": "CHART",
            "query_id": qry_id,
            "options": {
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
        }

        return self.post('visualizations', payload)

    def create_dashboard(self, name):
        payload = {
            "name": name
        }

        return self.post('dashboards', payload)

    def add_to_dashboard(self, db_id, vs_id, full_width=False):
        res = self.get(f"dashboards")

        slug = None
        for r in res.json()['results']:
            if r['id'] == db_id:
                slug = r['slug']
                break

        if slug:
            payload = {
                "dashboard_id": db_id,
                "visualization_id": vs_id,
                "width": 1,
                "options": {
                    "position": self.calculate_widget_position(slug, full_width)
                }
            }

            return self.post('widgets', payload)
        return "Dashboard not found."

    def calculate_widget_position(self, slug, full_width):
        position = {
            "col": 0,
            "row": 0,
            "sizeX": 3,
            "sizeY": 8
        }

        res = self.get(f'dashboards/{slug}')
        widgets = res.json()['widgets']

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

    def get_dashboard_public_url(self, db_id):
        try:
            self.post(f"dashboards/{db_id}", {"is_draft": False})
            res = self.post(f"dashboards/{db_id}/share")
            public_url = res.json()['public_url']
        except Exception as e:
            raise e

        return public_url
