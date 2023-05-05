from ProjectApp.courses.courses_element import CourseElement
import flask_unittest
from ProjectApp import create_app
import requests

class TestAPIElements(flask_unittest.ClientTestCase):
    app = create_app()
    #tests run in alphabetical order
    def testA_get_courses_elements(self, client):
        resp = client.get("/api/course-elements/")
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
        self.assertIsNotNone(json["next_page"])
        self.assertIsNone(json["previous_page"])

    def testB_get_course_element(self, client):
        resp = client.get("/api/course-elements/?course_id=420-110-DW&element_id=2")
        self.assertEqual(resp.status_code, 200)
    
    def testC_dont_get_course_element(self, client):
        resp = client.get("/api/course-elements/?course_id=test&element_id=3")
        self.assertEqual(resp.status_code, 404)  
        
    def testD_post_course_element(self, client):
        resp = client.get('/api/course-elements/')
        self.assertEqual(resp.status_code, 200) 
        course__element = CourseElement("420-110-DW", 9, 8.0).to_json()
        resp = client.post("/api/course-elements/", json = course__element)
        self.assertEqual(resp.status_code, 201)
        
    def testE_post_bad_course_element(self, client):
        resp = client.get('/api/course-elements/')
        self.assertEqual(resp.status_code, 200) 
        course__elements = resp.json
        course__element = course__elements["results"][0]
        course__element["course_id"] = None
        course__element["element_id"] = None
        resp = client.post("/api/course-elements/", json = course__element)
        self.assertEqual(resp.status_code, 409)
        
    def testF_update_course(self, client):
        resp = client.get('/api/course-elements/420-110-DW/9')
        self.assertEqual(resp.status_code, 200) 
        course__element = resp.json
        course__element["hours"] = 9.0
        resp = client.put("/api/course-elements/420-110-DW/9", json = course__element)
        self.assertEqual(resp.status_code, 204)
    
    def testG_delete_course_element(self, client):
        resp = client.get('/api/course-elements/420-110-DW/9')
        self.assertEqual(resp.status_code, 200)
        resp = client.delete("/api/course-elements/420-110-DW/9")
        self.assertEqual(resp.status_code, 204)
        resp = client.get('/api/course-elements/420-110-DW/9')
        self.assertEqual(resp.status_code, 404)

        
    # #     #python -m unittest

    def testH_dont_delete_course_element(self, client):
        resp = client.get('/api/course-elements/420-110-DW/9')
        self.assertEqual(resp.status_code, 404)
        resp = client.delete("/api/course-elements/420-110-DW/9")
        self.assertEqual(resp.status_code, 409)