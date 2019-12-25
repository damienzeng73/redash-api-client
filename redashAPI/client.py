import json
import requests

class RedashAPIClient(object):
    def __init__(self, api_key: str, host: str='http://localhost:5000'):
        self.api_key = api_key
        self.host = host

        self.s = requests.Session()
        self.s.headers.update({"Authorization": f"Key {api_key}"})

    def get(self, uri: str):
        res = self.s.get(f"{self.host}/api/{uri}")

        if res.status_code != 200:
            raise Exception(f"Retrieve data from URL: /api/{uri} failed.")

        return res

    def post(self, uri: str, payload: dict={}):
        data = json.dumps(payload)

        self.s.headers.update({"Content-Type": "application/json"})
        res = self.s.post(f"{self.host}/api/{uri}", data=data)

        if res.status_code != 200:
            raise Exception(f"Post data to URL: /api/{uri} failed.")

        return res

    def delete(self, uri: str):
        res = self.s.delete(f"{self.host}/api/{uri}")

        if res.status_code != 200:
            raise Exception(f"Delete data from URL: /api/{uri} failed.")

        return res

    def create_data_source(self, _type: str, name: str, options: dict={}):
        payload = {
            "type": _type,
            "name": name,
            "options": options
        }

        return self.post('data_sources', payload)

    def create_query(self, ds_id: int, name: str, qry: str, desc: str="", with_results: bool=True, options: dict={}):
        payload = {
            "data_source_id": ds_id,
            "name": name,
            "query": qry,
            "description": desc,
            "options": options
        }

        res = self.post('queries', payload)
        qry_id = res.json().get('id', None)

        if with_results:
            if qry_id is None:
                raise Exception("Failed to create query.")

            self.generate_query_results(qry_id)
        return res

    def refresh_query(self, qry_id: int):
        return self.post(f"queries/{qry_id}/refresh")

    def generate_query_results(self, qry_id: int):
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

    def create_visualization(self, qry_id: int, _type: str, name: str, columns: list=[], x_axis: str=None, y_axis: list=[], group_by: str=None, custom_options: dict={}, desc: str=None):
        if _type == 'table':
            if not columns or len(columns) == 0:
                try:
                    columns = custom_options['columns']
                except:
                    raise Exception("columns is reqruied for table.")

            order = 100000
            table_columns = []
            for idx, col in enumerate(columns):
                if 'name' not in col or 'type' not in col:
                    raise Exception("Missing name and type in columns.")

                table_columns.append({
                    "alignContent": "left",
                    "allowHTML": True,
                    "allowSearch": False,
                    "booleanValues": [False, True],
                    "dateTimeFormat": "DD/MM/YY HH:mm",
                    "displayAs": "string",
                    "highlightLinks": False,
                    "imageHeight": "",
                    "imageTitleTemplate": "{{ @ }}",
                    "imageUrlTemplate": "{{ @ }}",
                    "imageWidth": "",
                    "linkOpenInNewTab": True,
                    "linkTextTemplate": "{{ @ }}",
                    "linkTitleTemplate": "{{ @ }}",
                    "linkUrlTemplate": "{{ @ }}",
                    "numberFormat": "0,0",
                    "order": order + idx,
                    "title": col.get('title', col['name']),
                    "visible": True,
                    **col
                })

            chart_type = 'TABLE'
            options = {
                "autoHeight": True,
                "defaultColumns": 3,
                "defaultRows": 15,
                "itemsPerPage": 10,
                "minColumns": 1,
                "columns": table_columns,
                **custom_options
            }

        elif _type == 'pivot':
            if not custom_options:
                raise Exception("custom_options is required.")

            chart_type = 'PIVOT'
            options = custom_options

        else:
            if x_axis is None or len(y_axis) == 0:
                raise Exception("x_axis and y_axis is required.")

            seriesOptions = {}
            columnMapping = {}
            for idx, y in enumerate(y_axis):
                if 'name' not in y:
                    raise Exception("Missing name in y_axis.")

                y_name = y['name']
                y_label = y.get('label', y_name)
                y_type = y.get('type', _type)

                columnMapping[y_name] = "y"
                seriesOptions[y_name] = {
                    "index": 0,
                    "type": y_type,
                    "name": y_label,
                    "yAxis": 0,
                    "zIndex": idx
                }

            if group_by is not None:
                columnMapping[group_by] = "series"

            chart_type = 'CHART'
            options = {
                "globalSeriesType": _type,
                "sortX": True,
                "legend": {"enabled": True},
                "yAxis": [{"type": "linear"}, {"type": "linear", "opposite": True}],
                "xAxis": {"type": "category", "labels": {"enabled": True}},
                "error_y": {"type": "data", "visible": True},
                "series": {"stacking": None, "error_y": {"type": "data", "visible": True}},
                "seriesOptions": seriesOptions,
                "columnMapping": {x_axis: "x", **columnMapping},
                "showDataLabels": True if _type == 'pie' else False,
                **custom_options
            }

        payload = {
            "name": name,
            "type": chart_type,
            "query_id": qry_id,
            "description": desc,
            "options": options
        }

        return self.post('visualizations', payload)

    def create_dashboard(self, name: str):
        payload = {
            "name": name
        }

        return self.post('dashboards', payload)

    def add_widget(self, db_id: int, text: str="", vs_id: int=None, full_width: bool=False, position: dict=None):
        res = self.get(f"dashboards")

        results = res.json().get('results', [])
        slug = next((d['slug'] for d in results if d['id'] == db_id), None)

        if slug is None:
            raise Exception("Dashboard not found.")

        payload = {
            "dashboard_id": db_id,
            "text": text,
            "visualization_id": vs_id,
            "width": 1,
            "options": {
                "position": position or self.calculate_widget_position(slug, full_width)
            }
        }

        return self.post('widgets', payload)

    def calculate_widget_position(self, slug: str, full_width: bool):
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

    def publish_dashboard(self, db_id: int):
        try:
            self.post(f"dashboards/{db_id}", {"is_draft": False})
        except Exception as e:
            raise e

        res = self.post(f"dashboards/{db_id}/share")
        public_url = res.json().get('public_url', None)

        return public_url
