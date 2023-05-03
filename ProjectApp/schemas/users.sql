create table users (
    id NUMBER GENERATED ALWAYS as IDENTITY primary key,
    email VARCHAR2(100) NOT NULL,
    password VARCHAR2(102) NOT NULL,
    name VARCHAR2(1000) NOT NULL,
    member_type VARCHAR2(30) DEFAULT 'member'
); 

INSERT INTO users (email,password,name,member_type) VALUES ('instructor@dawsoncollege.qc.ca','dawson1234', 'Dirk', 'super_admin')
