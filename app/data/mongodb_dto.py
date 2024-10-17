from pydantic import BaseModel

# sample dto for mongoDB 
class Resume(BaseModel):
    name: str
    experience: list
    skills: list
    projects: list
    