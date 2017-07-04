import json
import pandas as pd

data = pd.read_csv('source_data/Mauritania_4Visual_mockup_063007.csv').dropna()

schools = []
towers  = []
connections = []

school_columns = ['IDORDRE', 'Wilaya', 'Moughataa', 'Commune', 'Type',
                  'Milieu', 'School Code', 'Name of the school', 'Locality Code',
                  'Classrooms', 'Divisions', 'Students', 'Teachers', 'Water',
                  'Electricity', 'Latrines', 'Tower_Distance', 'Type of Service',
                  'Tower Details']

tower_columns  = ['Type of Service',
                  'Tower Details']

line_columns   = [ 'Tower Details', 'Tower_Distance']
issues = []

for index, row in data.iterrows():
        
    school_coords = [row['LON'],row['LAT']]
    tower_coords  = [row['Tower_Longitude'],row['Tower_Latitude']]
    tower_id      = row['Tower Details']
    school_id     = int(index)

    if row['LAT'] <0:
        issues.append(row)
        school_coords=[row['LAT'],row['LON']]

    school_props = row[school_columns]
    school_props['school_id'] = school_id

    schools.append({
        'geometry':{
            'type':'Point',
            'coordinates': school_coords
        },
        'properties': school_props.to_dict(),
        
        'type':'Feature'
    })

    towers.append({
        'geometry':{
            'type':'Point',
            'coordinates': tower_coords
        },
        'properties': row[tower_columns].to_dict(),
        'type':'Feature'
    })

    connections.append({
        'geometry':{
            'type':'LineString',
            'coordinates': [school_coords,tower_coords]
        },
        'properties':{
            'Tower ID': tower_id,
            'school_id': school_id
        },

        'type':'Feature'
    })


def wrap_features(features):
    return {'type':'FeatureCollection', 'features': features}

with open('data/pc_schools.geojson','w') as s:
    
    json.dump(wrap_features(schools),s, sort_keys=True,
                      indent=4, separators=(',', ': '))

with open('data/pc_towers.geojson','w') as s:
    json.dump(wrap_features(towers),s, sort_keys=True,
                      indent=4, separators=(',', ': '))

with open('data/pc_connections.geojson','w') as s:
    json.dump(wrap_features(connections),s,sort_keys=True,
                      indent=4, separators=(',', ': '))

pd.DataFrame(issues).to_csv('data/pc_flipped_lat_lng_rows.csv')
