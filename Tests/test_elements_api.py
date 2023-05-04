import flask_unittest
from ProjectApp import create_app

class TestAPIElements(flask_unittest.ClientTestCase):
    app = create_app()
    def test_get_elements(self, client):
        resp = client.get('/api/elements')
        self.assertEqual(resp.status_code, 200)
        
        json = resp.json
        
        self.assertIsNotNone(json)
        self.assertIsNotNone(json["next_page"])
        self.assertIsNone(json["previous_page"])
        
    def test_post_element(self, client):
        resp = client.get('/api/elements')
        self.assertEqual(resp.status_code, 200) 
        elements = resp.json
        element = elements["results"][0]
        element["element_id"] = None
        
        resp = client.post("/api/elements", json = element)
        
        self.assertEqual(resp.status_code, 201)
    
    def test_get_element(self, client):
        resp = client.get('/api/elements/1')
        self.assertEqual(resp.status_code, 200)
        
        element = resp.json
        
        self.assertIsNotNone(element)
        self.assertEqual(element["element"], "Analyze the problem.")
    
    def test_update_element(self, client):
        resp = client.get('/api/elements/2')
        self.assertEqual(resp.status_code, 200)
        
        #setting new values for element
        element = resp.json
        element["element"] = "New element Name !"
        element["element_criteria"] = "Best New Criteria!"
        
        resp = client.put("/api/elements/2", json = element)
        
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(element["element_id"], 2)
        self.assertEqual(element["element_criteria"],"Best New Criteria!")
        
    def test_post_put_element(self, client):
        resp = client.get('/api/elements/3')
        self.assertEqual(resp.status_code, 200)
        element = resp.json
        self.assertIsNotNone(element)
        element["element_id"] = None #setting new id so its like a newly created element
        element["element"] = "New element Name for the element 70"
        
        resp = client.put("/api/elements/3", json = element)
        
        self.assertEqual(resp.status_code, 201)
        
        
    