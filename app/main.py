from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "hello"}

@app.get("/about")
def read_about():
    return {"message": "new message about"}


PRICES = {"SQURPHARMA": 212.4, "BATBC": 540.0, "GP": 305.3, "ROBI": 35.3}


@app.get("/prices/{ticker}")
def read_price(ticker: str):
    if ticker not in PRICES:
        raise HTTPException(status_code=404, detail="Ticker not found")
    return {"ticker": ticker, "price": PRICES[ticker]}

@app.get("/prices")
def read_all_prices():
    return PRICES