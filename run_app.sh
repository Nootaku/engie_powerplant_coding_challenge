if  [[ $1 = "--co2" ]]; then
CO2=True uvicorn app.main:app --host 0.0.0.0 --port 8888 --reload
else
uvicorn app.main:app --host 0.0.0.0 --port 8888 --reload
fi
