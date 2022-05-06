"""API ENDPOINTS

In the context of the Engie SPaaS powerplant-coding-challenge. This file
contains the endpoints for the requested API.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pathlib import Path
import logging
import app.models as models
import app.logic as logic

# Setup logging
logging.config.fileConfig(Path.cwd() / 'app' / 'logging.conf')
_logger_ = logging.getLogger('root')

# Initialize API
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/productionplan")
async def get_production_plan(payload: models.LoadRequest):
    try:
        response = logic.calculate_production_plan(payload)
        return JSONResponse(
            status_code=200,
            content=response
        )

    except ValueError as e:
        _logger_.error(
            'Target energy generation has not been reached.\n'
            f'Remaining Value {str(e)}'
        )
        return JSONResponse(
            status_code=500,
            content={
                'message': 'Target energy generation has not been reached.',
                'remaining_value': str(e)
            }
        )

    except Exception as e:
        _logger_.error(str(e))
        return JSONResponse(
            status_code=500,
            content=str(e)
        )
