DataPreparation.ipynb prepares and shreds data into multiple relations.
create.sql specifies SQL schema and restrictions on relations.
load.sql loads csv files to virtual machine.
setup.sh sets up sql database on VM.

You should first transfer the data folder, create.sql, load.sql, and setup.sh to your VM.
Suppose you put everything mentioned above into the folder /opt/dbcourse/gtd/. 
To set up the database called gtd, you should issue this command in VM shell:
/opt/dbcourse/gtd/setup.sh