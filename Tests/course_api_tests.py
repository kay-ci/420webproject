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
        
    def test_post_course(self, client):
        resp = client.get('/api/courses/add')
        self.assertEqual(resp.status_code, 200) 
        courses = resp.json
        course3 = courses["results"][0]
        course3["course_id"] = "3333333333"
        course1 = Course("1111111111", "any", 3.0, 3.0, 3.0, "any", 1, 1).to_json()
        course2 = {"course_id": "2222222222", "course_title": "any", "description": "any", "domain_id": 1, "lab_hours": 3.0, "term_id": 1, "theory_hours": 3.0, "work_hours": 3.0}
        resp = client.post("/api/courses/add", json = course1)
        self.assertEqual(resp.status_code, 201)
        resp = client.post("/api/courses/add", json = course2)
        self.assertEqual(resp.status_code, 201)
        resp = client.post("/api/courses/add", json = course3)
        self.assertEqual(resp.status_code, 201)
        
    def test_post_bad_course(self, client):
        resp = client.get('/api/courses/add')
        self.assertEqual(resp.status_code, 200) 
        
        courses = resp.json
        course = courses["results"][0]
        course["course_id"] = None
        resp = client.post("/api/courses/add", json = course)
        self.assertEqual(resp.status_code, 409)
    
    def test_delete_course(self, client):
        resp = client.get('/api/courses/delete/3333333333')
        self.assertEqual(resp.status_code, 200)
        course = resp.json
        self.assertIsNotNone(course)
        resp = client.delete("/api/courses/delete/3333333333")
        self.assertEqual(resp.status_code, 204)
        resp = client.delete("/api/courses/delete/1111111111")
        self.assertEqual(resp.status_code, 204)
        resp = client.delete("/api/courses/delete/2222222222")
        self.assertEqual(resp.status_code, 204)
        
        #python -m unittest

    def test_dont_delete_course(self, client):
        resp = client.get('/api/courses/delete/3333333333')
        self.assertEqual(resp.status_code, 404)
        resp = client.delete("/api/courses/delete/3333333333")
        self.assertEqual(resp.status_code, 409)