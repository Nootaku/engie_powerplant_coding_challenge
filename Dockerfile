# No need to make it complicated, right (KISS !)
# Documentation at:
# https://fastapi.tiangolo.com/deployment/docker/?h=docker#dockerfile

FROM python:3.10

# To minimize image size ... requirements first
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Then the code
WORKDIR /app
COPY ./app .

# And run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
