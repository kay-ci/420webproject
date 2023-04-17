create table users (
    id NUMBER GENERATED ALWAYS as IDENTITY primary key,
    email VARCHAR2(100) NOT NULL,
    password VARCHAR2(102) NOT NULL,
    name VARCHAR2(1000) NOT NULL,
    avatar_path VARCHAR2(2000),
    member_type VARCHAR2(30) DEFAULT 'Member'
); 

