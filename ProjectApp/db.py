from .competencies.competency import Competency
from .domains.domain import Domain
from .user import User
import oracledb
import os
from .elements.element import Element
from .courses.course import Course

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
        with self.__connection.cursor() as cursor:
            results = cursor.execute("select course_id, course_title, theory_hours, lab_hours, work_hours, description, domain_id, term_id from courses where course_id=:given_id", given_id=id)
            for row in results:
                course = Course(row[0], row[1], float(row[2]), float(row[3]), float(row[4]), row[5], int(row[6]), int(row[7]))
            return course
        
    def get_course_def(self, courseid):
        with self.__connection.cursor() as cursor:
            output = []
            results = cursor.execute("select unique competency_id, competency, competency_achievement, competency_type from VIEW_COURSES_ELEMENTS_COMPETENCIES where course_id=:id", id=courseid)
            for row in results:
                output.append(Competency(row[0], row[1], row[2], row[3]))
            return output

    def add_course(course):
        pass
    
    def get_domain(self, domain_id):
        with self.__connection.cursor() as cursor:
            results = cursor.execute('select domain, domain_description from domains where domain_id=:id', id=domain_id)
            for row in results:
                domain = Domain(domain_id,row[0],row[1])
                return domain; 
            
    def insert_domain(self, domain):
        if not isinstance(domain, Domain):
            raise TypeError()
        with self.__connection.cursor() as cursor:
            cursor.execute('insert into domains (domain_id, domain, domain_description) values (:domain_id,        :domain, :domain_description)',
                           domain_id = domain.domain_id, domain = domain.domain, domain_description = domain.domain_description)
    
    def get_domains(self):
        domains = []
        with self.__connection.cursor() as cursor:
            result = cursor.execute('select domain_id, domain, domain_description from domains')
            for row in result:
                domain = Domain(row[0],row[1],row[2])
                domains.append(domain)
        return domains
    
    def get_users(self):
        users = []
        with self.__connection.cursor() as cursor:
            result = cursor.execute('select email, password, name, member_type from users')
            for row in result:
                user = User(row[0],row[1],row[2])
                user.member_type = row[3]
                users.append(user)
        return users
    
    def get_user(self, email):
         with self.__connection.cursor() as cursor:
            results = cursor.execute('select email, password, name, member_type from users where email=:email', email=email)
            for row in results:
                user = User(row[0], row[1], row[2])
                user.member_type = row[3]
                return user
            
    def insert_user(self, user):
        if not isinstance(user, User):
            raise TypeError()
        # Insert the post to the DB
        with self.__connection.cursor() as cursor:
            cursor.execute('insert into users (email, password, name) values (:email, :password, :name)',
                           email=user.email, password=user.password, name=user.name)
    
    def get_user_id(self, id):
        with self.__connection.cursor() as cursor:
            results = cursor.execute('select email, password, id, name from users where id=:id', id=id)
            for row in results:
                user = User(row[0], row[1], row[3])
                user.id = row[2]
                return user

    
    def get_competencies(self):
        from .competencies.competency import Competency
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
        from .competencies.competency import Competency
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
    
    def update_competency(self, old_competency_id, competency_id, competency, competency_achievement, competency_type):
        from .competencies.competency import Competency
        fromDb = self.get_competency(old_competency_id)
        if fromDb == None:
            raise ValueError("couldn't find a competency with that id to update")
        newCompetency = Competency(competency_id, competency, competency_achievement, competency_type)#for the validation
        with self.__connection.cursor() as cursor:
            cursor.execute("update competencies set competency_id = :id, competency = :competency, competency_achievement = :achievement, competency_type = :type where competency_id = :old_id",
                           old_id = old_competency_id,
                           id = competency_id,
                           competency = competency,
                           achievement = competency_achievement,
                           type = competency_type)

    def add_competency(self, competency):
        from .competencies.competency import Competency
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
            results = cursor.execute("select element_id, element_order, element, element_criteria, competency_id from view_competencies_elements where competency_id = :id", id = id)
            for row in results:
                output.append(Element(row[0], row[1], row[2], row[3], row[4]))
        return output
                
    def get_courses_elements(self):
        from .courses.courses_element import CourseElement
        courses_elements = []
        with self.__get_cursor() as cursor:
            results = cursor.execute("select course_id, element_id, element_hours from courses_elements")
            for row in results:
                courses_elements.append(CourseElement(row[0], int(row[1]), float(row[2])))
        return courses_elements
    
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

    def get_elements(self):
        elements = []
        with self.__get_cursor() as cursor:
            results = cursor.execute("select element_id, element_order, element, element_criteria, competency_id from elements")
            for row in results:
                elements.append(Element(int(row[0]), int(row[1]), row[2], row[3], row[4]))
        return elements
    
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
        #check integrity todo
        with self.__get_cursor() as cursor:
            cursor.execute("insert into elements (element_id, element_order, element, element_criteria, competency_id) values (:id, :order, :element, :criteria, :comp_id)",
                           id = element.element_id,
                           order = element.element_order,
                           element = element.element,
                           criteria = element.element_criteria,
                           comp_id = element.competency_id)
    def update_element(self, element_id, element_order, element, element_criteria, competency_id ):
        check = self.get_element(int(element_id))
        if check == None:
            raise Exception("Could not update! element does not exist")
        with self.__get_cursor() as cursor:
            cursor.execute("update elements set element_order = :order, element = :element, element_criteria = :criteria, competency_id = :comp_id where element_id = :old_id",
                           order = element_order,
                           element = element,
                           criteria = element_criteria,
                           comp_id = competency_id,
                           old_id = element_id)
    def delete_element(self, element_id):
        element = self.get_element(int(element_id))
        if element == None:
            raise ValueError("Element does not exist could not delete!")
        with self.__get_cursor() as cursor:
            cursor.execute("delete from elements where element_id = :id", id = element_id )
    def get_terms(self):
        from .terms.term import Term
        output = []
        with self.__connection.cursor() as cursor:
            results = cursor.execute("select term_id, term_name from terms")
            for row in results:
                output.append(Term(row[0], row[1]))
        return output
    
    def get_term(self, id):#might return None
        output = None
        if not isinstance(id, int):
            raise TypeError("id must be an int")
        from .terms.term import Term
        with self.__connection.cursor() as cursor:
            results = cursor.execute("select term_id, term_name from terms where term_id = :id", id = id)
            for row in results:
                output = Term(row[0], row[1])
            return output

if __name__ == '__main__':
    print('Provide file to initialize database')
    file_path = input()
    if os.path.exists(file_path):
        db = Database()
        db.run_file(file_path)
        db.close()
    else:
        print('Invalid Path')
