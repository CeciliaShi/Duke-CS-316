# Folders explained

`app`: includes the flask web application

app/
	Ploty/ (mainly python scripts for generating plotly urls)
	static/ (webpage thing, including css, font, js and img)
	templates/ (website html templates)
	app.py (main flask script)
	cache.pickle (pickle object for caching default url)
	config.py (flask config)
	cache_plot.py (python script for generating cache.pickle)
	models.py (python script for interacting with relations in databse)
	plotly_conf.py (config file for plotly)

`database`: includes setup scripts for the database

database/
	create.sql (create tables)
	load.sql (load csv into database)
	Preprocess.py (process globalterrorismdb_0617dist.xlsx in to 7 csv's)
	setup.sh (setup script for databse)

# Instruction on generating the "production" dataset

## 1. Download all (8) csv files from [dropbox](https://www.dropbox.com/sh/z8erhydvfj85kj6/AAA5KLGdEDDBrNYbXveVmyzZa?dl=0) 

Alternative: request data from [umd](https://www.start.umd.edu/gtd/contact/) to get the .xlsx file (we have one available on [dropbox](https://www.dropbox.com/s/j6f6rjkcdf6qvu7/globalterrorismdb_0617dist.xlsx?dl=0)). Notice you still need to download `GoogleTrend.csv` from the [first dropbox link](https://www.dropbox.com/s/vz4u1eevos8on80/GoogleTrend.csv?dl=0)


## 2. Log into the vm and clone our github repo under `/opt/dbcourse/`:

```bash
$ cd /opt/dbcourse/
$ git clone https://github.com/hs220/Duke-CS-316.git
```

## 3. Copy all (8) csv files into your vm to `/opt/dbcourse/Duke-CS-316/source\ code/database/data`

If you go on 1. Alternative, copy the excel file (example would be `globalterrorismdb_0617dist.xlsx`) and `GoogleTrend.csv` to `/opt/dbcourse/Duke-CS-316/source\ code/database/data` and then run 

```bash
$ python Preprocess.py --fname data/globalterrorismdb_0617dist.xlsx
```

The script will generate 7 csv files which are the same from the drop box.

## 4. Make `setup.sh` executable by running commands at below:

```bash
$ cd /opt/dbcourse/Duke-CS-316/source\ code/database/
$ sudo chmod +x setup.sh
```

## 5. Run `setup.sh`:
```bash
$ /opt/dbcourse/Duke-CS-316/source\ code/database/setup.sh
```

Then the database is ready!

# Instruction on running the web app

## 1. Make sure you have set up the database as indicated in the last section

## 2. On your vm, run `app.py`

```bash
$ cd /opt/dbcourse/Duke-CS-316/source\ code/app
$ python app.py
```

\*Notice, if your vm is on google cloud, make sure to add `-L 5000:localhost -L` to your ssh command.

## 3. Open your browser and go to http://127.0.0.1:5000/ or http://localhost:5000
