from pydantic import BaseModel

from enum import Enum


class EmployeeFields(str, Enum):
    EMPLOYEE_ID = "MitarbeiterID"
    NAME = "Name"
    ROLE = "Rolle/Position"
    DEPARTMENT = "Abteilung"
    SKILLS = "Skills/Kompetenzen"
    PAST_PROJECTS = "Vergangene Projekte"
    EXTERNAL_EXPERIENCE = "Unternehmens-externe Erfahrung"
    CERTIFICATIONS = "Zertifizierungen"
    LANGUAGES = "Sprachen"
    LOCATION = "Standort"
    INTERESTS = "Interessen"
    DESCRIPTION = "Beschreibung"


class Employee(BaseModel):
    employee_id: str
    name: str
    role: str
    department: str
    skills: list[str]
    past_projects: list[str]
    external_experience: list[str]
    certifications: list[str]
    languages: list[str]
    location: str
    interests: list[str]
    description: str

    class Config:
        @staticmethod
        def alias_generator(field: str) -> str:
            return EmployeeFields[field.upper()].value
