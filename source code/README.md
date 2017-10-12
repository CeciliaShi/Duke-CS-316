1. Create a new folder to store the files.
2. On terminal, type nano and create a file called create.sql that copies everything from the create.sql from our source code file.
3. On terminal, type the follow:
	dropdb GTD;
	createdb GTD;
	psql GTD -af create.sql


This source code folder contains the following files:
1. create.sql: the file that creates the sample database including creating tables and contraints and inserting data.
2. test-sample.sql: the file that contains SQL queries that will supply contents for the web page.
	The queires are hard-coded with examples of parameters that the user selects.
3. test-sample.out: results of running test-sample.sql over the sample database.
4. DataPreparation.ipynb: python file for tranforming the real data.
5. app: this is the file that contains the html and python file for the web. We used flask to do the website.
		In order to get to the website, you need to do the following:
		* cd app
		* pip install flask
		* python app.py
		* A message will pop out: Running on http://127.0.0.1:5000/ (Press CTRL+C to quit), open a browser and go to http://127.0.0.1:5000/

