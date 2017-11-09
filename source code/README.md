# Instruction on generating the "production" dataset

## 1. Download all (8) csv files from [dropbox](https://www.dropbox.com/sh/z8erhydvfj85kj6/AAA5KLGdEDDBrNYbXveVmyzZa?dl=0) 

Alternative: request data from [umd](https://www.start.umd.edu/gtd/contact/) to get the excel file (we have one available on [dropbox](https://www.dropbox.com/s/j6f6rjkcdf6qvu7/globalterrorismdb_0617dist.xlsx?dl=0)). Notice you still need to download `comments.csv` from the [first dropbox link](https://www.dropbox.com/sh/z8erhydvfj85kj6/AAA5KLGdEDDBrNYbXveVmyzZa?dl=0)


## 2. Log into the vm and clone our github repo under `/opt/dbcourse/`:

```bash
$ cd /opt/dbcourse/
$ git clone https://github.com/hs220/Duke-CS-316.git
```
## 3. Copy all (8) csv files into your vm to `/opt/dbcourse/Duke-CS-316/source\ code/database/`

If you go on 1. Alternative, copy the excel file (example would be `globalterrorismdb_0617dist.xlsx`) and `comments.csv` to `/opt/dbcourse/Duke-CS-316/source\ code/database/` and then run 

```bash
$ python Preprocess.py --fname globalterrorismdb_0617dist.xlsx
```

The script will generate 7 csv files which are the same from the drop box.

## 4. Make `setup.sh` executable by running commands at below:

```bash
$ cd /opt/dbcourse/source\ code/database/
$ sudo chmod +x setup.sh
```

## 5. Run `setup.sh`:
```bash
$ /opt/dbcourse/source\ code/database/setup.sh
```

Then the database is ready!
