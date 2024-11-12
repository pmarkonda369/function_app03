import azure.functions as func
import logging
import json
from bot import generate_openai_response  # Ensure this import is correct

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Azure Function has received a request.')

    # Initialize `query` variable
    query1 = None

    # Attempt to retrieve `query` from query parameters or JSON body
    try:
        query1 = req.params.get('query')
        if not query1:
            req_body = req.get_json()
            query1 = req_body.get('query')
    except ValueError:
        logging.error("Failed to parse JSON body")

    # Check if `query` has a value
    if query1:
        logging.info(f"Received query: {query1}")
        try:
            # Generate response using the function
            bot_response = generate_openai_response(query1)
            logging.info(f"Bot Response: {bot_response}")
            return func.HttpResponse(f"Bot Response: {bot_response}")
        except Exception as e:
            logging.error(f"Error in generate_openai_response: {e}")
            return func.HttpResponse("Error generating bot response.", status_code=500)
    else:
        logging.warning("No query provided in the request.")
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )
