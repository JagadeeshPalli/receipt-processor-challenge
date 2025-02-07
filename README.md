This is a FastAPI-based web service that processes receipts and calculates reward points based on specific rules. The API includes endpoints for submitting receipts and retrieving their corresponding points.

Features:
1. Accepts receipt details via a POST request.
2. Calculates reward points based on predefined rules.
3. Allows retrieval of points via a GET request.
4. Fully Dockerized for easy deployment.

You can install the necessary dependencies in the requirements.txt file using the following command:
 > pip install -r requirements.txt

You can run the Fast API Application using the following command:
 > python - m uvicorn main:app --reload

After running the Fast API, you can test the API using the following link:

http://127.0.0.1:8000/docs

