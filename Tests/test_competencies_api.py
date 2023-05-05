import flask_unittest
from ProjectApp import create_app

class TestCompetencyAPI(flask_unittest.ClientTestCase):
    app = create_app()
    def test_competencies(self, client):
        resp = client.get('/api/competencies')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
        self.assertIsNotNone(json['next_page'])
        self.assertIsNone(json['prev_page'])

    def test_post_and_delete_competency(self, client):
        #setup code (adds a test competency to db)
        competency_with_elements = {"id":"test", "competency":"test-name", "competency_achievement":"test-achievement", "competency_type":"Mandatory"}
        elements = []
        elements.append({"element":"test-name", "element_criteria":"test criteria"})
        elements.append({"element":"test-name2", "element_criteria":"test criteria2"})
        competency_with_elements["elements"] = elements
        resp = client.post('/api/competencies', json=competency_with_elements)
        self.assertEqual(resp.status_code, 201)

        resp = client.delete('api/competencies/test')
        self.assertEqual(resp.status_code, 204)
    
    def test_put_update_competency(self, client):
        #setup code (adds a test competency to db)
        competency_with_elements = {"id":"test", "competency":"test-name", "competency_achievement":"test-achievement", "competency_type":"Mandatory"}
        elements = []
        elements.append({"element":"test-name", "element_criteria":"test criteria"})
        elements.append({"element":"test-name2", "element_criteria":"test criteria2"})
        competency_with_elements["elements"] = elements
        resp = client.post('/api/competencies', json=competency_with_elements)
        self.assertEqual(resp.status_code, 201)

        competency_with_elements["competency"] = "updated name"
        resp = client.put('api/competencies/test', json = competency_with_elements)
        self.assertEqual(resp.status_code, 201)

        #cleanup code (removes test competency from db)
        resp = client.delete('api/competencies/test')
        self.assertEqual(resp.status_code, 204)

    def test_put_new_competency(self, client):
        competency_with_elements = {"id":"test", "competency":"test-name", "competency_achievement":"test-achievement", "competency_type":"Mandatory"}
        elements = []
        elements.append({"element":"test-name", "element_criteria":"test criteria"})
        elements.append({"element":"test-name2", "element_criteria":"test criteria2"})
        competency_with_elements["elements"] = elements
        resp = client.put('api/competencies/test', json = competency_with_elements)
        self.assertEqual(resp.status_code, 201)

        #cleanup code (removes test competency from db)
        resp = client.delete('api/competencies/test')
        self.assertEqual(resp.status_code, 204)

    def test_get_competency(self, client):
        #setup code (adds a test competency to db)
        competency_with_elements = {"id":"test", "competency":"test-name", "competency_achievement":"test-achievement", "competency_type":"Mandatory"}
        elements = []
        elements.append({"element":"test-name", "element_criteria":"test criteria"})
        elements.append({"element":"test-name2", "element_criteria":"test criteria2"})
        competency_with_elements["elements"] = elements
        resp = client.post('/api/competencies', json=competency_with_elements)
        self.assertEqual(resp.status_code, 201)

        resp = client.get('api/competencies/test')
        self.assertEqual(resp.status_code, 200)

        #cleanup code (removes test competency from db)
        resp = client.delete('api/competencies/test')
        self.assertEqual(resp.status_code, 204)