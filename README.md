# powerplant-coding-challenge

[![Developer](https://img.shields.io/badge/Developer-Maxime&nbsp;Wattez-informational?style=for-the-badge&logo=GitHub&logoColor=white)](https://github.com/Nootaku)

[![Vue](https://img.shields.io/badge/Framework-FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=#009688)](https://vuejs.org/)

You can find the original README [here](documentation/README.md)

## Running the app

### Installation

This installation guide has been written under the assumption that you have Python 3.10 and PIP3 installed. If that is not the case, you can find the documentation to do so at:

- Python 3.10: [here](https://www.python.org/downloads/)
- PIP3: [here](https://pip.pypa.io/en/stable/)

```shell
# Cloning the project
git clone <url> powerplant_coding_challenge
cd powerplant_coding_challenge

# Installing dependencies
pip install -r requirements.txt

# Change permissions on shell-script for execution
chmod 700 run_app.sh
```

### Run the application

```shell
# To run without taking CO2 price into account
./run_app.sh

# To run with CO2 price
./run_app.sh --co2
```

## Explanation

### Architecture

I wanted to use a simplified version of a scallable architecture. Based on a MVC, I created the endpoints (`main.py`), the business logic (`logic.py`) and the models (`models.py`).

The models only serve the purpose of validating incoming requests and sending a `status_code: 422` if the request body was not conform.

In the business logic, I kept it in a single file. For a larger application, however, I would have split the code to facilitate code maintenance.

### Framework

FastAPI is relatively new, but is easy to setup and to use without compromising with performances or customizability.

### Logic

My objective was to produce the `load` while minimizing the price AND the energy waste.

To do so, I used a few steps:

1. Calculate the price per MWh for each powerplant
2. Order the powerplants by ascending production cost
3. Generate energy by looping throught the sorted list while taking the following into account:

- If the `pmax` of a powerplant can not be produced (remaining `load` is smaller than `pmax`), produce all the remaining load by current powerplant.
- If the `pmax` can be produced, first verify if the `pmin` of the next powerplant (`index + 1`) can be produced without any reminder. This means that if `rl = remaining_load - powerplant.pmax` we need to ensure that `rl - next_powerplant.pmin >=0`.
  - When the conditions above apply, use the current powerplant `pmax` else don't do anything.

4. Return the production results as a JSON

### Dockerfile

I tried to keep it as simple as possible.
This Dockerfile does not take the CO2 into account but could be by adding `ENV CO2=True` before the `CMD` instruction.

Also I know that the image could be even smaller if we were to use a multi-stage instruction, but that would be overkill for such a small project.
