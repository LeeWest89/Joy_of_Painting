from flask import Flask, jsonify, request
import mysql.connector
from fuzzywuzzy import process

app = Flask(__name__)

# Database configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'JoyOfPaintingDB'
}

# Colors from Colors_Used Table
valid_colors = ['Black_Gesso', 'Bright_Red', 'Burnt_Umber', 'Cadmium_Yellow', 'Dark_Sienna', 
                'Indian_Red', 'Indian_Yellow', 'Liquid_Black', 'Liquid_Clear', 'Midnight_Black', 
                'Phthalo_Blue', 'Phthalo_Green', 'Prussian_Blue', 'Sap_Green', 'Titanium_White', 
                'Van_Dyke_Brown', 'Yellow_Ochre', 'Alizarin_Crimson']

# Subjects from Subject_Matter Table
valid_subjects = ['APPLE_FRAME', 'AURORA_BOREALIS', 'BARN', 'BEACH', 'BOAT', 'BRIDGE', 'BUILDING', 
                      'BUSHES', 'CABIN', 'CACTUS', 'CIRCLE_FRAME', 'CIRRUS', 'CLIFF', 'CLOUDS', 'CONIFER', 
                      'CUMULUS', 'DECIDUOUS', 'DIANE_ANDRE', 'DOCK', 'DOUBLE_OVAL_FRAME', 'FARM', 'FENCE', 
                      'FIRE', 'FLORIDA_FRAME', 'FLOWERS', 'FOG', 'FRAMED', 'GRASS', 'GUEST', 
                      'HALF_CIRCLE_FRAME', 'HALF_OVAL_FRAME', 'HILLS', 'LAKE', 'LAKES', 'LIGHTHOUSE', 
                      'MILL', 'MOON', 'MOUNTAIN', 'MOUNTAINS', 'NIGHT', 'OCEAN', 'OVAL_FRAME', 
                      'PALM_TREES', 'PATH', 'PERSON', 'PORTRAIT', 'RECTANGLE_3D_FRAME', 
                      'RECTANGULAR_FRAME', 'RIVER', 'ROCKS', 'SEASHELL_FRAME', 'SNOW', 
                      'SNOWY_MOUNTAIN', 'SPLIT_FRAME', 'STEVE_ROSS', 'STRUCTURE', 'SUN', 
                      'TOMB_FRAME', 'TREE', 'TREES', 'TRIPLE_FRAME', 'WATERFALL', 'WAVES', 
                      'WINDMILL', 'WINDOW_FRAME', 'WINTER', 'WOOD_FRAMED']

# Establish database connection
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

# Route
@app.route('/episodes', methods=['GET'])
def get_episodes():
    month = request.args.get('month')
    subjects_param = request.args.get('subjects')
    colors_param = request.args.get('colors')

    query = "SELECT e.* FROM Episodes e"
    conditions = []
    params = []

    if month:
        conditions.append("e.month = %s")
        params.append(month)

    if subjects_param:
        subjects = [subject.strip() for subject in subjects_param.split(',')]
        # Fuzzy matching
        matched_subjects = set()
        for subject in subjects:
            matched_subject = process.extractOne(subject, valid_subjects)[0]
            if matched_subject:
                matched_subjects.add(matched_subject)

        if not matched_subjects:
            return jsonify({"error": "No valid subject found"}), 400
        
        subquery_conditions = [f"s.{subject} = 1" for subject in matched_subjects]
        conditions.append(f"e.id IN (SELECT id FROM Subject_Matter s WHERE {' AND '.join(subquery_conditions)})")

    if colors_param:
        colors = [color.strip() for color in colors_param.split(',')]
        # Fuzzy matching
        matched_colors = set()
        for color in colors:
            matched_color = process.extractOne(color, valid_colors)[0]
            if matched_color:
                matched_colors.add(matched_color)

        if not matched_colors:
            return jsonify({"error": "No valid color found"}), 400

        subquery_conditions = [f"c.{color} = 1" for color in matched_colors]
        conditions.append(f"e.id IN (SELECT id FROM Colors_Used c WHERE {' AND '.join(subquery_conditions)})")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, tuple(params))
    episodes = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(episodes)

if __name__ == '__main__':
    app.run(debug=True)