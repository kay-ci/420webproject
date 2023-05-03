from .competencies.competency import Competency
from .domains.domain import Domain
from flask import flash
from .users.user import User
import oracledb
import os
from .elements.element import Element
from .courses.course import Course
from .terms.term import Term

class Database:
    def __init__(self, autocommit=True):
        self.__connection = self.__connect()
        self.__connection.autocommit = autocommit

    def run_file(self, file_path):
        statement_parts = []
        with self.__connection.cursor() as cursor:
            with open(file_path, 'r') as f:
                for line in f:
                    statement_parts.append(line)
                    if line.strip('\n').strip('\n\r').strip().endswith(';'):
                        statement = "".join(
                            statement_parts).strip().rstrip(';')
                        if statement:
                            try:
                                cursor.execute(statement)
                            except Exception as e:
                                print(e)
                        statement_parts = []

    def close(self):
        '''Closes the connection'''
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None

    def __get_cursor(self):
            for i in range(3):
                try:
                    return self.__connection.cursor()
                except Exception as e:
                    # Might need to reconnect
                    self.__reconnect()

    def __reconnect(self):
        try:
            self.close()
        except oracledb.Error as f:
            pass
        self.__connection = self.__connect()

    def __connect(self):
        return oracledb.connect(user=os.environ['DBUSER'], password=os.environ['DBPWD'],
                                             host="198.168.52.211", port=1521, service_name="pdbora19c.dawsoncollege.qc.ca")
        
    def get_courses(self):
        with self.__connection.cursor() as cursor:
            cursor.execute("select course_id, course_title, theory_hours, lab_hours, work_hours, description, domain_id, term_id from courses")
            results = cursor.fetchall()
            addresses = []
            for row in results:
                address = Course(row[0], row[1], float(row[2]), float(row[3]), float(row[4]), row[5], int(row[6]), int(row[7]))
                addresses.append(address)
            return addresses
        
    def get_course(self, id):
        course = None
        with self.__connection.cursor() as cursor:
            results = cursor.execute("select course_id, course_title, theory_hours, lab_hours, work_hours, description, domain_id, term_id from courses where course_id=:given_id", given_id=id)
            for row in results:
                course = Course(row[0], row[1], float(row[2]), float(row[3]), float(row[4]), row[5], int(row[6]), int(row[7]))
        return course
        
    def get_course_competency(self, courseid):
        with self.__connection.cursor() as cursor:
            output = []
            results = cursor.execute("select unique competency_id, competency, competency_achievement, competency_type from VIEW_COURSES_ELEMENTS_COMPETENCIES where course_id=:id", id=courseid)
            for row in results:
                output.append(Competency(row[0], row[1], row[2], row[3]))
            return output

    def add_course(self, course):
        if not isinstance(course, Course):
            raise TypeError()
        if self.get_course(course.course_id) != None:
            raise ValueError("this id is already being used by an existing course")
        with self.__connection.cursor() as cursor:
            cursor.execute('insert into courses (course_id, course_title, theory_hours, lab_hours, work_hours, description, domain_id, term_id) values (:course_id, :course_title, :theory_hours, :lab_hours, :work_hours, :description, :domain_id, :term_id)',
                           course_id=course.course_id, course_title=course.course_title, theory_hours=course.theory_hours, lab_hours=course.lab_hours, work_hours=course.work_hours, description=course.description, domain_id=course.domain_id, term_id=course.term_id)
    
    def del_course(self, id):
        course = self.get_course(id)
        if course == None:
            raise ValueError("can't delete course, course does not exist")
        with self.__connection.cursor() as cursor:
            cursor.execute("delete from courses where course_id=:id", id = id)
            
    def update_course(self, course):
        with self.__get_cursor() as cursor:
            cursor.execute("update courses set course_title=:course_title, theory_hours=:theory_hours, lab_hours=:lab_hours, work_hours=:work_hours, description=:description, domain_id=:domain_id, term_id=:term_id where course_id=:course_id",
                           course_id=course.course_id, course_title=course.course_title, theory_hours=course.theory_hours, lab_hours=course.lab_hours, work_hours=course.work_hours, description=course.description, domain_id=course.domain_id, term_id=course.term_id)
            
    def get_domain(self, domain_id):
        domain = None
        with self.__connection.cursor() as cursor:
            results = cursor.execute('select domain, domain_description from domains where domain_id=:id', id=domain_id)
            for row in results:
                domain = Domain(domain_id,row[0],row[1])
        return domain
            
    def add_domain(self, domain):
        if not isinstance(domain, Domain):
            raise TypeError()
        if self.get_domain(domain.domain_id) != None:
            raise ValueError("this domain id is already being used")
        with self.__connection.cursor() as cursor:
            cursor.execute('insert into domains (domain, domain_description) values (:domain, :domain_description)', domain = domain.domain, domain_description = domain.domain_description)
    
    def get_domains(self):
        domains = []
        with self.__connection.cursor() as cursor:
            result = cursor.execute('select domain_id, domain, domain_description from domains order by domain_id')
            for row in result:
                domain = Domain(row[0],row[1],row[2])
                domains.append(domain)
        return domains
    
    def update_domain(self, domain):
        if not isinstance(domain, Domain):
            raise TypeError("expecting an arugment of type Domain")
        if self.get_domain(domain.domain_id) == None:
            raise ValueError("can't find domain with this id")
        with self.__get_cursor() as cursor:
            cursor.execute("update domains set domain = :domain, domain_description = :domain_description where domain_id = :domain_id", domain = domain.domain, domain_description = domain.domain_description, domain_id  = domain.domain_id)
    
    def delete_domain(self, id):
        if not isinstance(id, int):
            raise TypeError("expecting an argument of type int")
        if self.get_domain(id) == None:
            raise ValueError("could not find domain with this id")
        with self.__get_cursor() as cursor:
            cursor.execute("delete from domains where domain_id = :domain_id", domain_id = id)

    def get_domain_courses(self, id):
        courses = []
        if not isinstance(id, int):
            raise TypeError("expecting an argument of type int")
        domain = self.get_domain(id)
        if domain == None:
            raise ValueError("could not find domain with this id")
        with self.__get_cursor() as cursor:
            results = cursor.execute("select course_id, course_title, theory_hours, lab_hours, work_hours, description, domain_id, term_id from courses where domain_id = :domain_id", domain_id = domain.domain_id)
            for row in results:
                courses.append(Course(row[0], row[1], float(row[2]), float(row[3]), float(row[4]), row[5], row[6], row[7]))
        return courses

    def get_users(self):
        users = []
        with self.__connection.cursor() as cursor:
            result = cursor.execute('select email, password, name, member_type from USERS')
            for row in result:
                user = User(row[0],row[1],row[2])
                user.member_type = row[3]
                users.append(user)
        return users
    
    def get_user(self, email):
         with self.__connection.cursor() as cursor:
            results = cursor.execute('select email, password, name, member_type, id from USERS where email=:email', email=email)
            for row in results:
                user = User(row[0], row[1], row[2])
                user.member_type = row[3]
                user.id = row[4]
                return user
            
    def insert_user(self, user):
        if not isinstance(user, User):
            raise TypeError()
        # Insert the post to the DB
        with self.__connection.cursor() as cursor:
            cursor.execute('insert into USERS (email, password, name) values (:email, :password, :name)',
                           email=user.email, password=user.password, name=user.name)
    
    def get_user_id(self, id):
        with self.__connection.cursor() as cursor:
            results = cursor.execute('select email, password, id, name, member_type from USERS where id=:id', id=id)
            for row in results:
                user = User(row[0], row[1], row[3])
                user.id = row[2]
                user.member_type = row[4]
                return user
            
    def promote_user(self, user):
        with self.__get_cursor() as cursor:
            cursor.execute("update USERS set member_type = :new_member_type where email=:email",
                           new_member_type = 'admin',
                           email = user.email)
    
    def demote_user(self, user):
        with self.__get_cursor() as cursor:
            cursor.execute("update USERS set member_type = :new_member_type where email=:email",
                           new_member_type = 'member',
                           email = user.email)

    def delete_user(self, user):
        with self.__get_cursor() as cursor:
            cursor.execute("delete from USERS where email=:email", email=user.email)

    def get_competencies(self):
        output = []
        with self.__connection.cursor() as cursor:
            results = cursor.execute("select competency_id, competency, competency_achievement, competency_type from competencies")
            for row in results:
                output.append(Competency(row[0], row[1], row[2], row[3]))
        return output
    
    def get_competency(self, id):#might return None
        output = None
        if not isinstance(id, str):
            raise TypeError("id must be a string")
        with self.__connection.cursor() as cursor:
            results = cursor.execute("select competency_id, competency, competency_achievement, competency_type from competencies where competency_id = :id", id = id)
            for row in results:
                output = Competency(row[0], row[1], row[2], row[3])
            return output
    
    def delete_competency(self, id):
        competency = self.get_competency(id)#performs validation of type for id
        if competency == None:
            raise ValueError("can't delete competency that wasn't there to begin with")
        with self.__connection.cursor() as cursor:
            cursor.execute("delete from competencies where competency_id = :id", id = id)
    
    def update_competency(self, competency_id, competency, competency_achievement, competency_type):
        fromDb = self.get_competency(competency_id)
        if fromDb == None:
            raise ValueError("couldn't find a competency with that id to update")
        newCompetency = Competency(competency_id, competency, competency_achievement, competency_type)#for the validation
        with self.__connection.cursor() as cursor:
            cursor.execute("update competencies set competency = :competency, competency_achievement = :achievement, competency_type = :type where competency_id = :id",
                           id = competency_id,
                           competency = competency,
                           achievement = competency_achievement,
                           type = competency_type)

    def add_competency(self, competency):
        if not isinstance(competency, Competency):
            raise TypeError("expecting first argument to be an instance of Competency")
        fromDb = self.get_competency(competency.id)
        if fromDb != None:
            raise ValueError("an existing competency is already using this id")
        with self.__connection.cursor() as cursor:
            cursor.execute("insert into competencies values(:id, :competency, :competency_achievement, :competency_type)",
                            id = competency.id,
                            competency = competency.competency,
                            competency_achievement = competency.competency_achievement, 
                            competency_type = competency.competency_type)
            
    def get_competency_elements(self, id):
        output = []
        if not isinstance(id, str):
            raise TypeError("id must be a string")
        from .elements.element import Element
        with self.__connection.cursor() as cursor:
            results = cursor.execute("select element_id, element_order, element, element_criteria, competency_id from view_competencies_elements where competency_id = :id order by element_order", id = id)
            for row in results:
                output.append(Element(row[0], row[1], row[2], row[3], row[4]))
        return output
    
    def get_next_competency_element_order(self, id):
        if not isinstance(id, str):
            raise TypeError("id must be a string")
        if self.get_competency(id) == None:
            raise ValueError("could not find a competency with given id")
        with self.__connection.cursor() as cursor:
            results = cursor.execute("select max(element_order) from elements where competency_id = :competency_id",
                                     competency_id = id)
            for row in results:
                if isinstance(row[0], int):
                    return row[0]+1
                return 1
    
    def delete_competency_element(self, competency_id, element):
        if not isinstance(element, Element):
            raise TypeError("expecting the 2nd argument to be of type Element")
        if not isinstance(competency_id, str):
            raise TypeError("competency id must be a string")
        if self.get_competency(competency_id) == None:
            raise ValueError("could not find a competency with given id")
        if self.get_element(element.element_id) == None:
            raise ValueError("could not find the element to delete given its id")
        with self.__get_cursor() as cursor:
            results = cursor.execute("select count(*) from elements where competency_id = :competency_id", competency_id = element.competency_id)
            for row in results:
                if row[0] <= 1:
                    raise ValueError("Cannot delete this element as it is the last one of its competency")
        with self.__get_cursor() as cursor:
            cursor.execute("delete from elements where element_id = :element_id", element_id = element.element_id)
            results = cursor.execute("select element_id, element_order, element, element_criteria, competency_id from elements where competency_id = :competency_id AND element_order > :deleted_order", competency_id = competency_id, deleted_order = element.element_order)
            for row in results:
                self.update_element(Element(row[0], row[1]-1, row[2], row[3], row[4]))

    def get_courses_elements(self):
        from .courses.courses_element import CourseElement
        courses_elements = []
        with self.__get_cursor() as cursor:
            results = cursor.execute("select course_id, element_id, element_hours from courses_elements order by course_id")
            for row in results:
                courses_elements.append(CourseElement(row[0], int(row[1]), float(row[2])))
        return courses_elements
    
    def get_elements_and_course_ids_as_tuples(self):
        from .courses.courses_element import CourseElement
        courses_elements = []
        with self.__get_cursor() as cursor:
            results = cursor.execute("select course_id, element_hours, element_id, element_order, element, element_criteria, competency_id from view_courses_elements order by course_id")
            for row in results:
                courses_elements.append((row[0], row[1], Element(row[2], row[3], row[4], row[5], row[6])))
        return courses_elements
    
    def calculate_course_hours(self, course_id):
        output = 0
        if not isinstance(course_id, str):
            raise TypeError("expecting a string id")
        if self.get_course(course_id) == None:
            raise ValueError("could not find a course for this id")
        with self.__get_cursor() as cursor:
            results = cursor.execute("select course_id, element_id, element_hours from courses_elements where course_id = :course_id", course_id = course_id)
            for row in results:
                output += row[2]
        return output
    
    def get_courses_with_sum_hours_from_elements(self):
        output = []
        courses = self.get_courses()
        for course in courses:
            output.append((course, self.calculate_course_hours(course.course_id)))
        return output

    def add_courses_element(self, course_element):
        with self.__get_cursor() as cursor:
            cursor.execute("insert into course_element values(:course_id, :elem_id, :elem_hours)",
                           course_id = course_element.course_id,
                           elem_id = course_element.element_id,
                           elem_hourse = course_element.hours)
    
    #only update hours
    def update_courses_element(self, course_element):
        with self.__get_cursor() as cursor:
            cursor.execute("update course_element set elem_hours = :new_hour where course_id=:id and elem_id = :elem_id",
                           new_hour = course_element.hours,
                           id = course_element.course_id,
                           elem_id = course_element.element_id)

    def get_elements(self, page_num=1, page_size=50):
        elements = []
        prev_page = None
        next_page = None
        offset = (page_num - 1) * page_size
        with self.__get_cursor() as cursor:
            results = cursor.execute("select element_id, element_order, element, element_criteria, competency_id from elements order by element_id offset :offset rows fetch next :page_size rows only",
                                     offset = offset,
                                     page_size = page_size)
            for row in results:
                elements.append(Element(int(row[0]), int(row[1]), row[2], row[3], row[4]))
        if page_num > 1:
            prev_page = page_num - 1
        if len(elements) > 0 and (len(elements) >= page_size):
            next_page = page_num + 1
        return elements, prev_page, next_page
    
    def get_element(self, element_id):
        if not isinstance (element_id, int):
            raise TypeError("element_id must be int")
        element = None
        with self.__get_cursor() as cursor:
            result = cursor.execute("select element_id, element_order, element, element_criteria, competency_id from elements where element_id = :id", id = element_id)
            for row in result:
                element = Element(int(row[0]), int(row[1]), row[2], row[3], row[4])
            return element
        
    def add_element(self, element):
        if not isinstance(element, Element):
            raise TypeError("Expected Type Element")
        with self.__get_cursor() as cursor:
            cursor.execute("insert into elements(element_order, element, element_criteria, competency_id) values(:element_order, :element, :element_criteria, :competency_id)",
                           element_order = element.element_order,
                           element = element.element,
                           element_criteria = element.element_criteria,
                           competency_id = element.competency_id)
    # change this method to take in an element instead
    def update_element(self, element):
        if not isinstance(element, Element):
            raise TypeError("expecting an argument of type Element")
        check = self.get_element(int(element.element_id))
        if check == None:
            raise Exception("Could not update! element does not exist")
        with self.__get_cursor() as cursor:
            cursor.execute("update elements set element_order=:element_order, element=:element, element_criteria=:criteria, competency_id=:compId where element_id=:id", element_order = element.element_order, element = element.element, criteria = element.element_criteria, compId = element.competency_id, id = element.element_id)
    def delete_element(self, element_id):
        element = self.get_element(int(element_id))
        if element == None:
            raise ValueError("Element does not exist could not delete!")
        with self.__get_cursor() as cursor:
            results = cursor.execute("select count(*) from elements where competency_id = :competency_id", competency_id = element.competency_id)
            for row in results:
                if row[0] <= 1:
                    raise ValueError("Cannot delete this element as it is the last one of its competency")
        with self.__get_cursor() as cursor:
            cursor.execute("delete from elements where element_id = :id", id = element_id)
            results = cursor.execute("select element_id, element_order, element, element_criteria, competency_id from elements where competency_id = :competency_id AND element_order > :deleted_order", competency_id = element.competency_id, deleted_order = element.element_order)
            for row in results:
                self.update_element(row[0], row[1]-1, row[2], row[3])
    def get_terms(self):
        output = []
        with self.__connection.cursor() as cursor:
            results = cursor.execute("select term_id, term_name from terms order by terms.term_id")
            for row in results:
                output.append(Term(row[0], row[1]))
        return output
    
    def get_term(self, id):#might return None
        output = None
        if not isinstance(id, int):
            raise TypeError("id must be an int")
        with self.__connection.cursor() as cursor:
            results = cursor.execute("select term_id, term_name from terms where term_id = :id", id = id)
            for row in results:
                output = Term(row[0], row[1])
            return output
        
    def get_term_courses(self, id):
        if not isinstance(id, int):
            raise TypeError("expecting an integer id parameter")
        if self.get_term(id) == None:
            raise ValueError("given id does not correspond to any term")
        output = []
        with self.__get_cursor() as cursor:
            results = cursor.execute("select course_id, course_title, theory_hours, work_hours, lab_hours, description, domain_id from view_courses_terms where term_id = :term_id", term_id = id)
            for row in results:
                output.append(Course(row[0], row[1], float(row[2]), float(row[3]), float(row[4]), row[5], row[6], id))
        return output
    
    def add_term(self, term):
        if not isinstance(term, Term):
            raise TypeError("expected type Term")
        with self.__get_cursor() as cursor:
            cursor.execute("insert into terms (term_name) values (:my_term_name)", my_term_name = str.capitalize(term.name))
            
    def update_term(self, term):
        if not isinstance(term, Term):
            raise TypeError("expected type Term")  
        with self.__get_cursor() as cursor:
            cursor.execute("update terms set term_name = :term_name where term_id = :term_id", term_name = str.capitalize(term.name), term_id = term.id)          
    
    def delete_term(self, id):
        if not isinstance(id, int):
            raise TypeError("expected type int")     
        with self.__get_cursor() as cursor:
            cursor.execute("delete from terms where term_id = :term_id", term_id = id)

if __name__ == '__main__':
    print('Provide file to initialize database')
    file_path = input()
    if os.path.exists(file_path):
        db = Database()
        db.run_file(file_path)
        db.close()
    else:
        print('Invalid Path')
