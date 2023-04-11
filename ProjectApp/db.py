import oracledb
import os
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
            
    def get_courses_elements(self):
        from .courses.courses_element import CourseElement
        courses_elements = []
        with self.__get_cursor() as cursor:
            results = cursor.execute("select course_id, elem_id, elem_hours from course_element")
            for row in results:
                courses_elements.append(CourseElement(row[0], row[1], float(row[2])))
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


if __name__ == '__main__':
    print('Provide file to initialize database')
    file_path = input()
    if os.path.exists(file_path):
        db = Database()
        db.run_file(file_path)
        db.close()
    else:
        print('Invalid Path')
