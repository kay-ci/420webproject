import flask_unittest
from courses import courses_api

class TestAPI(flask_unittest.ClientTestCase):
    app = create_app()
    def test_posts(self, client):
        resp = client.get('/api/courses/')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
        self.assertIsNotNone(json['next_page'])
        self.assertIsNone(json['prev_page'])
