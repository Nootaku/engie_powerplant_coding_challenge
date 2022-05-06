"""API MODELS

The data models accepted by the API as input (in request) as well as the data
models provided by the API as output (in response).
"""

from pydantic import BaseModel
from typing import List


class Powerplant(BaseModel):
    """Input (request) object of a powerplant."""
    name: str
    type: str
    efficiency: float
    pmin: int
    pmax: int

    class Config:
        """Example Powerplant data."""
        schema_extra = {
            'example': {
                'name': 'gasfiredbig1',
                'type': 'gasfired',
                'efficiency': 0.53,
                'pmin': 100,
                'pmax': 460
            }
        }


class LoadRequest(BaseModel):
    """Input (request) object."""
    load: int
    fuels: dict
    powerplants: List[Powerplant]

    class Config:
        """Example request json."""
        schema_extra = {
            'example': {
                "load": 480,
                "fuels": {
                    "gas(euro/MWh)": 13.4,
                    "kerosine(euro/MWh)": 50.8,
                    "co2(euro/ton)": 20,
                    "wind(%)": 60
                },
                "powerplants": [
                    {
                        "name": "gasfiredbig1",
                        "type": "gasfired",
                        "efficiency": 0.53,
                        "pmin": 100,
                        "pmax": 460
                    },
                    {
                        "name": "tj1",
                        "type": "turbojet",
                        "efficiency": 0.3,
                        "pmin": 0,
                        "pmax": 16
                    },
                    {
                        "name": "windpark1",
                        "type": "windturbine",
                        "efficiency": 1,
                        "pmin": 0,
                        "pmax": 150
                    }
                ]
            }
        }


class PowerplantLoad(BaseModel):
    """Object representing the output (response) load of a single powerplant.
    """
    name: str
    p: float

    class Config:
        """Example response json."""
        schema_extra = {
            'example': {
                'name': 'gasfiredbig1',
                'p': 40
            }
        }
