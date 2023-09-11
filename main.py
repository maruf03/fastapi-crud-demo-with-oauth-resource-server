from fastapi import FastAPI, Depends, Request, Response, status
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


from utils import VerifyToken

token_auth_scheme = HTTPBearer()
app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://localhost:*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ItemRequestBody(BaseModel):
    name: str
    description: str = None
    price: float

class ItemResponseBody(BaseModel):
    id: int
    name: str
    description: str = None
    price: float

items = [
    ItemResponseBody(id=1, name="Item 1", description="Item 1 description", price=10.0),
    ItemResponseBody(id=2, name="Item 2", description="Item 2 description", price=20.0),
    ItemResponseBody(id=3, name="Item 3", description="Item 3 description", price=30.0),
    ItemResponseBody(id=4, name="Item 4", description="Item 4 description", price=40.0),
    ItemResponseBody(id=5, name="Item 5", description="Item 5 description", price=50.0),
]
    
@app.get("/items")
async def read_items(response:Response, token: str = Depends(token_auth_scheme)):
    result = VerifyToken(token.credentials).verify()
    if result.get("status"):
       response.status_code = status.HTTP_400_BAD_REQUEST
       return result
    return items

@app.post("/items")
async def create_item(item: ItemRequestBody, response:Response, token: str = Depends(token_auth_scheme)):
    item = ItemResponseBody(id=len(items)+1, name=item.name, description=item.description, price=item.price)
    items.append(item) 
    response.status_code = status.HTTP_201_CREATED
    return item

@app.get("/items/{item_id}")
async def read_item(item_id: int, token: str = Depends(token_auth_scheme)):
    item = next((item for item in items if item.id == item_id), None)
    return item

@app.put("/items/{item_id}")
async def update_item(item_id: int, item:ItemRequestBody , token: str = Depends(token_auth_scheme)):
    #update item
    updated_item = ItemResponseBody(id=item_id, name=item.name, description=item.description, price=item.price)
    items[item_id-1] = updated_item
    return updated_item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int, response:Response , token: str = Depends(token_auth_scheme)):
    items.pop(item_id-1)
    response.status_code = status.HTTP_204_NO_CONTENT
    return 
