import json
import os
import responses
import unittest

from redashAPI import RedashAPIClient


class TestDashboard(unittest.TestCase):

    @responses.activate
    def test_get_dashboard_queries(self):
        # tested against Redash 8.0.0+b32245 (a16f551e)
        redash_host = os.getenv('REDASH_HOST')
        redash_api_key = os.getenv('REDASH_API_KEY')
        responses.add(responses.GET, '{}/api/dashboards/mocked_endpoint'.format(redash_host),
                      json=json.loads(MOCKED_RESPONSE), status=200)
        redash = RedashAPIClient(redash_api_key, redash_host)
        queries = redash.get_dashboard_queries('mocked_endpoint')
        assert len(responses.calls) == 1
        assert len(queries) == 1
        assert queries[0]['name'] == 'Name of the query'
        assert queries[0]['id'] == 244
        assert queries[0]['query'] == 'query;'


MOCKED_RESPONSE = """
{
"tags": [],
"is_archived": false,
"updated_at": "2021-06-03T18:09:05.062Z",
"is_favorite": false,
"user": {
    "auth_type": "external",
    "is_disabled": false,
    "updated_at": "2021-06-03T18:09:09.897Z",
    "profile_image_url": "https://www.gravatar.com/avatar/id",
    "is_invitation_pending": false,
    "groups": [
        2
    ],
    "id": 16,
    "name": "Name",
    "created_at": "2020-07-28T15:35:52.035Z",
    "disabled_at": null,
    "is_email_verified": true,
    "active_at": "2021-06-03T18:09:08Z",
    "email": "name@domain.com"
},
"layout": [],
"is_draft": true,
"id": 21,
"can_edit": true,
"user_id": 16,
"name": "Dashboard Name",
"created_at": "2021-06-03T18:09:05.062Z",
"slug": "dashboard_name",
"version": 1,
"widgets": [
    {
        "visualization": {
            "description": "",
            "created_at": "2021-05-25T13:22:32.811Z",
            "updated_at": "2021-06-03T18:09:40.878Z",
            "id": 320,
            "query": {
                "user": {
                    "auth_type": "external",
                    "is_disabled": false,
                    "updated_at": "2021-06-03T18:09:09.897Z",
                    "profile_image_url": "https://www.gravatar.com/avatar/id",
                    "is_invitation_pending": false,
                    "groups": [
                        2
                    ],
                    "id": 16,
                    "name": "Name",
                    "created_at": "2020-07-28T15:35:52.035Z",
                    "disabled_at": null,
                    "is_email_verified": true,
                    "active_at": "2021-06-03T18:09:08Z",
                    "email": "name@domain.com"
                },
                "created_at": "2021-05-25T13:22:32.811Z",
                "latest_query_data_id": 213928,
                "schedule": null,
                "description": null,
                "tags": [
                    "tag"
                ],
                "updated_at": "2021-05-28T11:19:53.467Z",
                "last_modified_by": {
                    "auth_type": "external",
                    "is_disabled": false,
                    "updated_at": "2021-06-03T18:09:09.897Z",
                    "profile_image_url": "https://www.gravatar.com/avatar/id",
                    "is_invitation_pending": false,
                    "groups": [
                        2
                    ],
                    "id": 16,
                    "name": "Name",
                    "created_at": "2020-07-28T15:35:52.035Z",
                    "disabled_at": null,
                    "is_email_verified": true,
                    "active_at": "2021-06-03T18:09:08Z",
                    "email": "name@domain.com"
                },
                "options": {
                    "parameters": []
                },
                "is_safe": true,
                "version": 1,
                "query_hash": "hash",
                "is_archived": false,
                "query": "query;",
                "api_key": "key",
                "is_draft": false,
                "id": 244,
                "data_source_id": 1,
                "name": "Name of the query"
            },
            "type": "TABLE",
            "options": {},
            "name": "Table"
        },
        "text": "",
        "created_at": "2021-06-03T18:09:40.878Z",
        "updated_at": "2021-06-03T18:09:43.370Z",
        "options": {
            "parameterMappings": {},
            "isHidden": false,
            "position": {
                "autoHeight": true,
                "sizeX": 3,
                "sizeY": 11,
                "maxSizeY": 1000,
                "maxSizeX": 6,
                "minSizeY": 1,
                "minSizeX": 2,
                "col": 0,
                "row": 0
            }
        },
        "dashboard_id": 21,
        "width": 1,
        "id": 139
    }
],
"dashboard_filters_enabled": false
}
"""
