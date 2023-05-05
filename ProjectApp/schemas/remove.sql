--drop tables
drop table courses_elements cascade constraints;
drop table elements cascade constraints;
drop table competencies cascade constraints;
drop table courses cascade constraints;
drop table terms cascade constraints;
drop table domains cascade constraints;
--Logging
drop table audit_logs cascade constraints;

--Drop Views
drop view view_courses;
drop view view_courses_elements;
drop view view_courses_terms;
drop view view_courses_domains;
drop view view_competencies;
drop view view_competencies_elements;
drop view view_courses_elements_competencies;

--Drop Package
drop package courses_package;

--Drop Object
drop type course_typ;
drop type term_typ;
drop type domain_typ;
drop type element_array;
drop type element_typ;
drop type competency_typ;
