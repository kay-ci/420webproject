import flask_unittest
from ProjectApp import create_app

class TestAPI(flask_unittest.ClientTestCase):
    app = create_app()
    def test_posts(self, client):
        resp = client.get('/api/domains/')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
        self.assertIsNotNone(json['next_page'])
        self.assertIsNone(json['prev_page'])

    def test_send_post(self, client):
        resp = client.get('/api/domains/')
        self.assertEqual(resp.status_code, 200)
        domains = resp.json
        
        domain = domains['results'][0]
        
        domain['domain'] = 'Programming, Data Structures, and Algorithms'

        resp = client.post('/api/domains/', json=domain)
        self.assertEqual(resp.status_code, 201)
