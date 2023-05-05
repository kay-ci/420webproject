import flask_unittest
from ProjectApp.dbmanager import get_db
from ProjectApp import create_app

class TestAPIDomains(flask_unittest.ClientTestCase):
    app = create_app()
    def test_get_domains(self, client):
        resp = client.get('/api/domains')
        self.assertEqual(resp.status_code, 200)
        
        json = resp.json
        
        self.assertIsNotNone(json)
        self.assertIsNotNone(json["next_page"])
        self.assertIsNone(json["previous_page"])
        
    def test_post_and_delete_domain(self, client):
        resp = client.get('/api/domains')
        self.assertEqual(resp.status_code, 200) 
        domains = resp.json
        domain = domains["results"][0]
        domain["domain_id"] = None
        domain["domain"] = "Testing API Post"
        domain["domain_description"] = "This is a test domain for the api unit test, this is fun!"
        
        resp = client.post("/api/domains", json = domain)
        self.assertEqual(resp.status_code, 201)
        #testing delete
        resp = client.delete(f"/api/domains/{get_db().get_domain_id()}")
        self.assertEqual(resp.status_code, 204) 
    
    def test_get_domain(self, client):
        resp = client.get('/api/domains/1')
        self.assertEqual(resp.status_code, 200)
        
        domain = resp.json
        
        self.assertIsNotNone(domain)
        self.assertEqual(domain["domain"], "Programming, Data Structures, and Algorithms")
    
    def test_update_domain(self, client):
        resp = client.get('/api/domains/2')
        self.assertEqual(resp.status_code, 200)
        
        #setting new values for domain
        domain = resp.json
        domain["domain"] = "New domain Name !"
        domain["domain_description"] = "Best new description for the updated api test"
        
        resp = client.put("/api/domains/2", json = domain)
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(domain["domain_id"], 2)
        self.assertEqual(domain["domain_description"],"Best new description for the updated api test")
        
    def test_post_put_domain(self, client):
        resp = client.get('/api/domains/3')
        self.assertEqual(resp.status_code, 200)
        domain = resp.json
        self.assertIsNotNone(domain)
        domain["domain_id"] = None #setting new id so its like a newly created domain
        domain["domain"] = "New API PUT domain POST"
        domain["domain_description"] = "This case test desprition is for PUT request when resource being updated does not exist"
        
        resp = client.put("/api/domains/3", json = domain)
        
        self.assertEqual(resp.status_code, 201)