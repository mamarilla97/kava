from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .settings import get_settings
from .schemas import Dish

settings = get_settings()
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

"""
FastAPI application main module.
This module contains the main FastAPI application instance and all route definitions.
It implements a simple CRUD API for managing dishes.
"""

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Main router
api_router = APIRouter(prefix=settings.API_V1_STR)

# Simulating a simple database with a list (in real case you would use a DB)
dishes_db = []

@api_router.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.
    Returns:
        dict: Welcome message
    """
    return {"message": "Welcome to the API!"}

@api_router.get("/health")
async def health_check():
    """
    Health check endpoint to verify API status.
    Returns:
        dict: Status confirmation
    """
    return {"status": "ok"}

@api_router.post("/dishes/", response_model=Dish, status_code=201)
async def create_dish(dish: Dish):
    """
    Create a new dish.
    Args:
        dish (Dish): The dish data to create
    Returns:
        Dish: The created dish
    """
    dishes_db.append(dish)
    return dish

@api_router.get("/dishes/", response_model=List[Dish])
async def get_dishes():
    """
    Get all dishes.
    Returns:
        List[Dish]: List of all dishes
    """
    return dishes_db

@api_router.get("/dishes/{dish_id}", response_model=Dish)
async def get_dish(dish_id: int):
    """
    Get a specific dish by ID.
    Args:
        dish_id (int): The ID of the dish to retrieve
    Returns:
        Dish: The requested dish
    Raises:
        HTTPException: If the dish is not found
    """
    dish = next((d for d in dishes_db if d.id == dish_id), None)
    if dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish

@api_router.put("/dishes/{dish_id}", response_model=Dish)
async def update_dish(dish_id: int, updated_dish: Dish):
    """
    Update an existing dish.
    Args:
        dish_id (int): The ID of the dish to update
        updated_dish (Dish): The new dish data
    Returns:
        Dish: The updated dish
    Raises:
        HTTPException: If the dish is not found
    """
    index = next((i for i, d in enumerate(dishes_db) if d.id == dish_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Dish not found")
    dishes_db[index] = updated_dish
    return updated_dish

@api_router.delete("/dishes/{dish_id}", status_code=204)
async def delete_dish(dish_id: int):
    """
    Delete a dish.
    Args:
        dish_id (int): The ID of the dish to delete
    Returns:
        None
    Raises:
        HTTPException: If the dish is not found
    """
    index = next((i for i, d in enumerate(dishes_db) if d.id == dish_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Dish not found")
    dishes_db.pop(index)
    return None

# Include routers in the application
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    """
    Startup event handler that prints the application mode.
    """
    print(f"Application started in {'debug' if settings.DEBUG else 'production'} mode")
