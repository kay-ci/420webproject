drop table users;

create table users (
    id NUMBER GENERATED ALWAYS as IDENTITY primary key,
    email VARCHAR2(100) NOT NULL,
    password VARCHAR2(102) NOT NULL,
    name VARCHAR2(1000) NOT NULL,
    member_type VARCHAR2(30) DEFAULT 'member'
); 

UPDATE users
SET MEMBER_TYPE = 'super_admin'
WHERE email = 'instructor@dawsoncollege.qc.ca';

commit;
