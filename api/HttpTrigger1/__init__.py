import azure.functions as func
import logging
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Try to get 'query' from request parameters or JSON body
    query = req.params.get('query')
    if not query:
        try:
            req_body = req.get_json()
            query = req_body.get('query')
        except ValueError:
            pass

    if query:
        return func.HttpResponse(f"Hello, {query}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )
