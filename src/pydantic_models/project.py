from pydantic import BaseModel
from enum import Enum


class ProjectFields(str, Enum):
    NAME = "Name"
    PROJECT_GOAL = "Projektziel"
    CONTENT = "Inhalt"
    SUCCESS = "Erfolg (Feedback)"
    DURATION = "Zeitlicher Umfang"
    BUDGET = "Budget"
    INDUSTRY = "Branche/Projektpartner"
    COMPANY = "Unternehmen"


class Project(BaseModel):
    name: str
    project_goal: str
    content: str
    success: str
    duration: str
    budget: str
    industry: str
    company: str

    class Config:
        @staticmethod
        def alias_generator(field: str) -> str:
            return ProjectFields[field.upper()].value


if __name__ == "__main__":
    project = Project(
        **{
            ProjectFields.NAME.value: "Test Project",
            ProjectFields.PROJECT_GOAL.value: "Test Project Goal",
            ProjectFields.CONTENT.value: "Test Content",
            ProjectFields.SUCCESS.value: "Test Success",
            ProjectFields.DURATION.value: "Test Duration",
            ProjectFields.BUDGET.value: "Test Budget",
            ProjectFields.INDUSTRY.value: "Test Industry",
            ProjectFields.COMPANY.value: "Test Company",
        }
    )
    # print the project with the aliases
    print(project.model_dump(by_alias=True))
