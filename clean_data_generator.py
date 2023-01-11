import pandas as pd

df = pd.read_csv('ErdbebenDaten.csv')
dff = df[['mag', 'depth', 'latitude', 'longitude', 'time', 'place']]

#place aufteilen und bereinigen
dff = pd.concat([dff, dff['place'].str.split(', ', expand=True)], axis=1)
dff = dff.drop(['place'], axis=1)
dff.rename(columns={0: 'place', 1: 'state', 2: 'unknown'}, inplace=True)

not_usa = dff[dff['unknown'].notnull()].index
dff = dff.drop(not_usa, axis=0)
dff = dff.drop(['unknown'], axis=1)

# time aufteilen in tage und uhrzeit sowie jahr als neues Attribut
dff = pd.concat([dff, dff['time'].str.split('T', expand=True)], axis=1)
dff = dff.drop(['time'], axis=1)
dff.rename(columns={0: 'date', 1: 'time'}, inplace=True)
dff['year'] = pd.DatetimeIndex(dff['date']).year

# State-Names vereinheitlichen
state_names = pd.read_csv('stateAbbreviations.csv')

dff['state'] = dff['state'].replace(['CA'],'California')
dff['state'] = dff['state'].replace(['NV'],'Nevada')
dff['state'] = dff['state'].replace(['UT'],'Utah')
dff['state'] = dff['state'].replace(['OK'],'Oklahoma')
dff['state'] = dff['state'].replace(['MO'],'Missouri')
dff['state'] = dff['state'].replace(['KS'],'Kansas')
dff['state'] = dff['state'].replace(['TN'],'Tennessee')
dff['state'] = dff['state'].replace(['TX'],'Texas')
dff['state'] = dff['state'].replace(['WA'],'Washington')
dff['state'] = dff['state'].replace(['ID'],'Idaho')
dff['state'] = dff['state'].replace(['MT'],'Montana')
dff['state'] = dff['state'].replace(['CO'],'Colorado')

"""
for element in dff['state']:
    if element in state_names['Code'].values:
        print(element)
"""

# Negative Werte in absolute umwandeln
dff['depth'] = dff['depth'].abs()

# Leere Staaten füllen
dff.loc[dff['state'].isnull(), 'state'] = dff['place']


# Weitere Probleme...
dff = dff.drop(dff[dff.state == 'Canada'].index)
dff = dff.drop(dff[dff.state == 'Mexico'].index)

for element in dff['state']:
    if element not in state_names['State'].values:
        for State in state_names['State'].values:
            if State in element:
                dff['state'] = dff['state'].replace([element], State)


for element in dff['state']:
    if element not in state_names['State'].values:
        dff = dff.drop(dff[dff.state == element].index)


dff.to_csv('clean_data.csv')
