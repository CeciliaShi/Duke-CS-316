import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import argparse
import logging
import sys

def read_xlsx(fname):
	return pd.read_excel(fname)

def preprocess(df):
	df = df.loc[df['latitude'].notnull() & df['longitude'].notnull()]
	# drop rows with na's in targsubtype1_txt and target1
	df = df.loc[df['targsubtype1_txt'].notnull() & df['target1'].notnull()]
	# drop rows with na's in gname
	df = df.loc[df['gname'].notnull()]
	# convert imonth=0 and iday=0 to missing value
	df.loc[df['imonth']==0,'imonth'] = None
	df.loc[df['iday']==0, 'iday'] = None
	return df

def writeIncident(df):
	Incident = df.loc[:,['eventid', 'iyear', 'imonth', 'iday', 'INT_LOG', 'property', 'nwound', 'nkill']]
	# add date
	Incident['date'] = pd.to_datetime({'year':df['iyear'], 
	                                        'month':df['imonth'],
	                                        'day':df['iday']})
	# drop year, month, and day
	Incident.drop(['iyear','imonth','iday'], inplace=True, axis=1)
	# rename colnames
	Incident.columns = ['id', 'international', 'property_damage', 'nwound', 'nkill', 'date']
	Incident.to_csv("Incident.csv", index=False, header=False)

def writeLocation(df):
	Location = df.loc[:,['latitude', 'longitude', 'country_txt', 'provstate', 'city']]
	# rename column names
	Location.columns = ['latitude', 'longitude', 'country', 'prov_state', 'city']
	# drop duplicates based on values of key
	Location.drop_duplicates(['latitude', 'longitude'], inplace=True)
	Location.to_csv("Location.csv", index=False, header=False, float_format='%.6f')

def writeHappened(df):
	Happened = df.loc[:,['eventid', 'latitude', 'longitude']]
	Happened.columns = ['incident_id', 'latitude', 'longitude']
	Happened.to_csv("Happened.csv", index=False, header=False, float_format='%.6f')

def writeTargeted(df):
	Targeted = df.loc[:,['eventid', 'targtype1_txt', 'targsubtype1_txt', 'target1']]
	Targeted.columns = ['incident_id', 'victim_type', 'subtype', 'target']
	Targeted.to_csv("Targeted.csv", index=False, header=False)

def writeBelongedTo(df):
	BelongedTo = df[['eventid', 'attacktype1_txt', 'success', 'suicide']]
	BelongedTo.columns = ['incident_id', 'attack_type', 'succussful_attack', 'suicide_attack']
	BelongedTo.to_csv("BelongedTo.csv", index=False, header=False)

def writeUsed(df):
	Used = df[['eventid', 'weaptype1_txt']]
	Used.columns = ['incident_id', 'weapon_type']
	Used.to_csv('Used.csv', index=False, header=False)

def writeInitiatedBy(df):
	InitiatedBy = df[['eventid', 'gname']]
	InitiatedBy.columns = ['incident_id', 'perpetrator_name']
	InitiatedBy.to_csv('InitiatedBy.csv', index=False,header=False)

def main(args):
	logging.basicConfig(level=logging.INFO, stream=sys.stdout)
	logging.info('Started')
	df = read_xlsx(args.fname)	
	logging.info('Finished reading {}'.format(args.fname))
	df = preprocess(df)
	logging.info('Finished preprocessing data')
	writeIncident(df)
	logging.info('Finished writing Incident.csv')
	writeLocation(df)
	logging.info('Finished writing Location.csv')
	writeHappened(df)
	logging.info('Finished writing Happened.csv')
	writeTargeted(df)
	logging.info('Finished writing Targeted.csv')
	writeBelongedTo(df)
	logging.info('Finished writing writeBelongedTo.csv')
	writeUsed(df)
	logging.info('Finished writing Used.csv')
	writeInitiatedBy(df)
	logging.info('Finished writing InitiatedBy.csv')
	logging.info('Finished!')


parser = argparse.ArgumentParser()
parser.add_argument('--fname', help='File to transfer', default = "globalterrorismdb_0617dist.xlsx")
args = parser.parse_args()

if __name__ == "__main__":
	main(args)