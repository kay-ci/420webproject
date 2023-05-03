import flask_unittest
from ProjectApp import create_app

class TestAPIElements(flask_unittest.ClientTestCase):
    app = create_app()
    def test_get_elements(self, client):
        resp = client.get('/api/elements/')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
        self.assertIsNotNone(json["next_page"])
        self.assertIsNone(json["previous_page"])
        
    def test_post_element(self, client):
        resp = client.get('/api/elements')
        self.assertEqual(resp.status_code, 200)
        posts = resp.json
        post = posts["results"][0]
        post["element_id"] = None
        
        resp = client.post("/api/elements", json = post)
        self.assertEqual(resp.status_code, 201)