import oracledb
import os
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

    
    def add_course(course):
        pass


if __name__ == '__main__':
    print('Provide file to initialize database')
    file_path = input()
    if os.path.exists(file_path):
        db = Database()
        db.run_file(file_path)
        db.close()
    else:
        print('Invalid Path')
