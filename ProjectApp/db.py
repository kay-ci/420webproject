from .domains.domain import Domain
from ProjectApp.user import User
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
    
    def get_domain(self, domain_id):
        with self.__connection.cursor() as cursor:
            results = cursor.execute('select domain, domain_description where domain_id=:id', domain_id=domain_id)
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
            result = cursor.execute('select email, password, name, avatar_path from users')
            for row in result:
                user = User(row[0],row[1],row[2], row[3])
                users.append(user)
        return users
    
    def get_user(self, email):
         with self.__conn.cursor() as cursor:
            results = cursor.execute('select email, password, id, name from users where email=:email', email=email)
            for row in results:
                user = User(row[0], row[1], row[3])
                user.id = row[2]
                return user
            
    def insert_user(self, user):
        if not isinstance(user, User):
            raise TypeError()
        # Insert the post to the DB
        with self.__conn.cursor() as cursor:
            cursor.execute('insert into users (email, password, name) values (:email, :password, :name)',
                           email=user.email, password=user.password, name=user.name)
    
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

if __name__ == '__main__':
    print('Provide file to initialize database')
    file_path = input()
    if os.path.exists(file_path):
        db = Database()
        db.run_file(file_path)
        db.close()
    else:
        print('Invalid Path')
