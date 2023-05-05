from ProjectApp.courses.course import Course
import flask_unittest
from ProjectApp import create_app

class TestAPIElements(flask_unittest.ClientTestCase):
    app = create_app()
    #tests run in alphabetical order
    def testA_get_courses(self, client):
        resp = client.get("/api/courses/")
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
        self.assertIsNone(json["next_page"])
        self.assertIsNone(json["previous_page"])

    def testB_get_course(self, client):
        resp = client.get("/api/courses/?id=420-210-DW")
        self.assertEqual(resp.status_code, 200)
    
    def testC_dont_get_course(self, client):
        resp = client.get("/api/courses/show?id=test")
        self.assertEqual(resp.status_code, 404)  
        
    def testD_post_course(self, client):
        resp = client.get('/api/courses/add')
        self.assertEqual(resp.status_code, 200) 
        course1 = Course("1111111111", "any", 3.0, 3.0, 3.0, "any", 1, 1).to_json()
        course2 = {"course_id": "2222222222", "course_title": "any", "description": "any", "domain_id": 1, "lab_hours": 3.0, "term_id": 1, "theory_hours": 3.0, "work_hours": 3.0}
        resp = client.post("/api/courses/add", json = course1)
        self.assertEqual(resp.status_code, 201)
        resp = client.post("/api/courses/add", json = course2)
        self.assertEqual(resp.status_code, 201)
        
    def testE_post_bad_course(self, client):
        resp = client.get('/api/courses/add')
        self.assertEqual(resp.status_code, 200) 
        courses = resp.json
        course = courses["results"][0]
        course["course_id"] = None
        resp = client.post("/api/courses/add", json = course)
        self.assertEqual(resp.status_code, 409)
        
    def testF_update_course(self, client):
        resp = client.get('/api/courses/update')
        self.assertEqual(resp.status_code, 200) 
        courses = resp.json
        course = courses["results"][0]
        course["course_id"] = "3333333333"
        resp = client.post("/api/courses/add", json = course)
        self.assertEqual(resp.status_code, 201)
        course["description"] = "anyanyany"
        resp = client.put("/api/courses/update", json = course)
        self.assertEqual(resp.status_code, 204)
    
    def testG_delete_course(self, client):
        resp = client.get('/api/courses/420-110-DW')
        self.assertEqual(resp.status_code, 200)

        resp = client.delete("/api/courses/1111111111")
        self.assertEqual(resp.status_code, 204)
        resp = client.delete("/api/courses/2222222222")
        self.assertEqual(resp.status_code, 204)
        resp = client.delete("/api/courses/3333333333")
        self.assertEqual(resp.status_code, 204)
        
        #python -m unittest

    def testH_dont_delete_course(self, client):
        resp = client.get('/api/courses/3333333333')
        self.assertEqual(resp.status_code, 404)
        resp = client.delete("/api/courses/3333333333")
        self.assertEqual(resp.status_code, 409)