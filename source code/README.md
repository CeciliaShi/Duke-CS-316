# Instruction on generating the "production" dataset

1. Download all data from [dropbox](https://www.dropbox.com/sh/z8erhydvfj85kj6/AAA5KLGdEDDBrNYbXveVmyzZa?dl=0)

2. Log into the vm and clone our github repo under `/opt/dbcourse/`:

```bash
$ cd /opt/dbcourse/
$ git clone https://github.com/hs220/Duke-CS-316.git
```
3. Copy all (8) `.csv` files into your vm (by `scp` commmand or `shared` folder) to `/opt/dbcourse/Duke-CS-316/source\ code/database/`

4. make `setup.sh` executable by running commands at below:

```bash
$ cd /opt/dbcourse/source\ code/database/
$ sudo chmod +x setup.sh
```

5. run `setup.sh`:
```bash
$ /opt/dbcourse/source\ code/database/setup.sh
```

Then the database is ready!
