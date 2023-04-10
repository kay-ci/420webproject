from domains.domain import Domain
import oracledb
import os

from user import User
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
            cursor.execute('insert into domains (domain_id, domain, domain_description) values (:domain_id, :domain, :domain_description)',
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

if __name__ == '__main__':
    print('Provide file to initialize database')
    file_path = input()
    if os.path.exists(file_path):
        db = Database()
        db.run_file(file_path)
        db.close()
    else:
        print('Invalid Path')
