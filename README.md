# ZCU FAV erasmus map

The goal of this project is to provide data on the ZCU FAV faculty partnership through the erasmus program.

It consist of a small web app using a flask (python) server for operations not available through client side javascript.

## Data

Source data files must be placed in a "sources" folder in the static folder.
They can be updated through the 'upload' page.

## To run

The project uses a small flask server to ruin on windows using powershell :

Declare the app

> $env:FLASK_APP = "erasmusMap"

Optional : For dev server (hot realoads ...)

> $env:FLASK_ENV = "development"

To run the launche the server

> flask run