"""API BUSINESS LOGIC

In the context of the Engie SPaaS powerplant-coding-challenge. This file
contains the logic for calculating the API responses.
"""
import app.models as models
import os


add_co2 = os.environ.get('CO2', 'False').lower() in ('true')


class Powerplant:
    def __init__(self, powerplant_dict):
        self.fuel_conversion_dict = {
            'gasfired': 'gas(euro/MWh)',
            'turbojet': 'kerosine(euro/MWh)',
            'windturbine': 'wind(%)'
        }
        self.name = powerplant_dict['name']
        self.type = powerplant_dict['type']
        self.fuel = self.fuel_conversion_dict[self.type]
        self.efficiency = powerplant_dict['efficiency']
        self.p_min = powerplant_dict['pmin']
        self.p_max = powerplant_dict['pmax']

    def fuel_cost(self, fuel_dict, CO2_emmissions=False):
        """Return the cost the plant fuel per generated MWh.

        The formula used for the cost calculation is:
            (1 / efficiency) * fuel_cost_per_mwh

        If CO2_emmissions is True, add the cost of CO2_emmissions for the fuel:
            + 0.3 * CO2_cost
        """
        fuel_cost_per_mwh = 0
        if self.type != 'windturbine':
            fuel_cost_per_mwh = fuel_dict[self.fuel]

        efficiency_multiplier = 1 / self.efficiency

        cost = efficiency_multiplier * fuel_cost_per_mwh

        if CO2_emmissions and self.type != 'windturbine':
            # each MWh generated creates 0.3 ton of CO2
            # means we base our emmissions on the output (not input)
            cost += 0.3 * fuel_dict['co2(euro/ton)']

        return cost

    def production_data(self, fuel_dict, CO2_emmissions=False):
        """Return an object with all the production data of current powerplant:
            - name
            - production cost per MWh
            - the minimum and maximum production values and costs
        """
        # Calculate fuel cost
        fuel_cost = self.fuel_cost(fuel_dict, CO2_emmissions)

        # Correct the wind energy efficiency
        if self.type == 'windturbine':
            self.p_min = self.p_min * (fuel_dict['wind(%)'] * 0.01)
            self.p_max = self.p_max * (fuel_dict['wind(%)'] * 0.01)

        # Return object with all powerplant stats
        return {
            'name': self.name,
            'cost_per_mwh': fuel_cost,
            'minimum_production': self.p_min,
            'minimum_production_cost': self.p_min * fuel_cost,
            'maximum_production': self.p_max,
            'maximum_production_cost': self.p_max * fuel_cost
        }


def calculate_production_plan(request_obj: models.LoadRequest):
    """For each powerplant in request_obj.powerplants, calculate the amount of
    energy that the powerplant should produce in order to reach the
    request_obj.load at the cheapest possile price.

    1. For each powerplant, calculate the cost of 1 MWh gereration
    2. Order powerplants by ascending production cost
    3. Loop through powerplants to produce maximum production (if possible)
       starting with the cheapest source.
    4. Return energy generation per powerplant
    """
    # Create a list of powerplants and calculate the min and max cost of each
    powerplant_list = []

    for powerplant in request_obj.powerplants:
        pp = Powerplant(powerplant.dict())
        powerplant_list.append(
            pp.production_data(request_obj.fuels, add_co2)
        )

    # Sort the list of powerplants per ascending min and max cost
    powerplant_list.sort(key=lambda powerplant_list: [
                powerplant_list['minimum_production_cost'],
                powerplant_list['maximum_production_cost']
                ])

    # Start generating energy for as cheap as possible without wasting energy
    energy_to_generate = request_obj.load  # MWh
    generated_energy = []

    for index, powerplant in enumerate(powerplant_list):
        # Calculate the difference between the (remaining) target and the max
        # production of a powerplant
        energy_diff = energy_to_generate - powerplant['maximum_production']

        # Ensure that the remainder is positive
        if energy_diff > 0:
            try:
                # If there is another powerplant in the list get his min prod.
                # and assert that its minimum production can be produced to
                # reach target without wasting energy.
                # If both conditions are met produce energy with cheaper source
                next_pmin = powerplant_list[index + 1]['minimum_production']
                if energy_diff >= next_pmin:
                    generated_energy.append(
                        {
                            'name': powerplant['name'],
                            'p': powerplant['maximum_production']
                        }
                    )
                    energy_to_generate -= powerplant['maximum_production']

            # If we get to the end of the list without reaching the target, we
            # raise an error
            except IndexError:
                generated_energy.append(
                    {
                        'name': powerplant['name'],
                        'p': powerplant['maximum_production']
                    }
                )
                energy_to_generate -= powerplant['maximum_production']
                raise ValueError(energy_to_generate)

        # If the previous conditions are not met, complete the
        elif energy_diff <= 0:
            generated_energy.append(
                {
                    'name': powerplant['name'],
                    'p': energy_to_generate
                }
            )
            break

        else:
            raise ValueError(energy_to_generate)

    return generated_energy
