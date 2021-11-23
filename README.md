# doa-api
Kumpulan doa-doa sesuai al-qur'an dan as-sunnah

## Requirements
- Python
- pip
- virtualenv 
- Flask
- Sastrawi

## How to Run
- Clone this repo
- ```cd doa-api```
- Activate the virtual environment ```source venv/bin/activate```
- ```export FLASK_ENV=development```
- ```flask run```
- Send GET request to http://localhost:5000/

## Endpoints
|Method|URI|Description|
|-|-|-|
|GET|[/all](https://tanyadoa-api.herokuapp.com/all)|Show all doa|
|GET|[/search/{keywords}](https://tanyadoa-api.herokuapp.com/search/doa+sebelum+makan)|Search doa by keywords|
|GET|[/show/{id_doa}](https://tanyadoa-api.herokuapp.com/show/1)|Show doa by ```id_doa```|


## Link
http://tanyadoa-api.herokuapp.com/
