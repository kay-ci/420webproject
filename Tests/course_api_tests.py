from ProjectApp.courses.course import Course
import flask_unittest
from ProjectApp import create_app
import requests

class TestAPIElements(flask_unittest.ClientTestCase):
    app = create_app()
    def test_get_elements(self, client):
        resp = client.get("/api/courses/show")
        self.assertEqual(resp.status_code, 200)
        
        json = resp.json
        
        self.assertIsNotNone(json)
        self.assertIsNone(json["next_page"])
        self.assertIsNone(json["previous_page"])

    def test_get_course(self, client):
        resp = client.get("/api/courses/show?id=420-210-DW")
        self.assertEqual(resp.status_code, 200)
    
    def test_dont_get_course(self, client):
        resp = client.get("/api/courses/show?id=test")
        self.assertEqual(resp.status_code, 404)  
        #feature/elements-api
        
    def test_post_course(self, client):
        resp = client.get('/api/courses/addcourse')
        self.assertEqual(resp.status_code, 200) 
        # courses = resp.json
        # course = courses["results"][0]
        # course["course_id"] = "None"
        course = Course("1111111111", "any", float(3), float(3), float(3), "any", int(1), int(1)).to_json()
        
        resp = client.post("/api/courses/addcourse", json = course)
        
        self.assertEqual(resp.status_code, 201)
        
        #python -m unittest

