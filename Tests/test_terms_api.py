import flask_unittest
from ProjectApp.dbmanager import get_db
from ProjectApp import create_app

class TestAPITerms(flask_unittest.ClientTestCase):
    app = create_app()
    def test_get_terms(self, client):
        resp = client.get('/api/terms')
        self.assertEqual(resp.status_code, 200)
        
        json = resp.json
        
        self.assertIsNotNone(json)
        self.assertIsNotNone(json["next_page"])
        self.assertIsNone(json["previous_page"])
        
    def test_post_term(self, client):
        resp = client.get('/api/terms')
        self.assertEqual(resp.status_code, 200) 
        terms = resp.json
        term = terms["results"][0]
        term["id"] = None
        term["name"] = "test"
        
        resp = client.post("/api/terms", json = term)
        
        self.assertEqual(resp.status_code, 201)
    
    def test_get_term(self, client):
        resp = client.get('/api/terms/1')
        self.assertEqual(resp.status_code, 200)
        
        term = resp.json
        
        self.assertIsNotNone(term)
        self.assertEqual(term["name"], "Fall")
    
    def test_update_term(self, client):
        resp = client.get('/api/terms/2')
        self.assertEqual(resp.status_code, 200)
        
        #setting new values for term
        term = resp.json
        term["name"] = "update"
        
        resp = client.put("/api/terms/2", json = term)
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(term["id"], 2)
        
    def test_post_put_element(self, client):
        resp = client.get('/api/elements/3')
        self.assertEqual(resp.status_code, 200)
        element = resp.json
        self.assertIsNotNone(element)
        element["element_id"] = None #setting new id so its like a newly created element
        element["element"] = "New API PUT element POST"
        element["element_order"] = get_db().get_next_competency_element_order(element["competency_id"])
        
        resp = client.put("/api/elements/3", json = element)
        
        self.assertEqual(resp.status_code, 201)