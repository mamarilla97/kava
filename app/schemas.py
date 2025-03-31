from pydantic import BaseModel

class Dish(BaseModel):
    id: int
    name: str
    precio: float
    
    class Config:
        from_attributes = True
        
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Pizza Margherita",
                "precio": 12.99
            }
        } 