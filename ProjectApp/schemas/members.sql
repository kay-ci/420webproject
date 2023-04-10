
create table members(
    id number GENERATED ALWAYS as IDENTITY primary key,
    email varchar2(100) NOT NULL,
    password varchar2(102) NOT NULL,
    name varchar2(1000) NOT NULL,
    avatar_path (2000)
);

