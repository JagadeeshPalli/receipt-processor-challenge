import math
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4

app = FastAPI()

# In-memory storage
receipts = {}

class Item(BaseModel):
    shortDescription: str
    price: str

class Receipt(BaseModel):
    retailer: str
    purchaseDate: str
    purchaseTime: str
    items: list[Item]
    total: str

def calculate_pts(receipt: Receipt):
    pts = 0

    #Rule 1: Retailer Name pts (1 point per alphanumeric character)
    pts += sum(c.isalnum() for c in receipt.retailer)

    #Rule 2: 50 pts if total is a round dollar amount
    total_amount = float(receipt.total)
    if total_amount.is_integer():
        pts += 50

    #Rule 3: 25 pts if total is a multiple of 0.25
    if total_amount % 0.25 == 0:
        pts += 25

    #Rule 4: 5 pts for every two items
    pts += (len(receipt.items) // 2) * 5

    #Rule 5: pts for items with descriptions of length multiple of 3
    for item in receipt.items:
        desc_len = len(item.shortDescription.strip())
        if desc_len % 3 == 0:
            pts += math.ceil(float(item.price) * 0.2)  # 20% of price, rounded up

    #Rule 6: 6 pts if purchase date is an odd day
    day = int(receipt.purchaseDate.split("-")[-1])
    if day % 2 != 0:
        pts += 6

    #Rule 7: 10 pts if purchase time is between 2:00 PM - 3:59 PM
    purchase_time = datetime.strptime(receipt.purchaseTime, "%H:%M")
    if 14 <= purchase_time.hour < 16:
        pts += 10

    return pts

@app.post("/receipts/process")
def process_receipt(receipt: Receipt):
    receipt_id = str(uuid4())
    receipts[receipt_id] = receipt
    return {"id": receipt_id}

@app.get("/receipts/{id}/points")
def get_pts(id: str):
    print("Stored Receipt IDs:", receipts.keys())
    print("Requested ID:", id)

    if id not in receipts:
        raise HTTPException(status_code=404, detail="No receipt found for that ID")

    pts = calculate_pts(receipts[id])
    return {"points": pts}

