import mysql.connector
import pandas as pd

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Rootuser1@',
    'database': 'JoyOfPaintingDB'
}

def create_tables(cursor):
    # Drop tables if they exist
    cursor.execute("DROP TABLE IF EXISTS Colors_Used;")
    cursor.execute("DROP TABLE IF EXISTS Subject_Matter;")
    cursor.execute("DROP TABLE IF EXISTS Episodes;")

    # Create Episodes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Episodes (
        episode_id INT AUTO_INCREMENT PRIMARY KEY,
        painting_title VARCHAR(255),
        painting_index INT,
        season INT,
        episode INT,
        date DATE,
        img_src VARCHAR(255),
        youtube_src VARCHAR(255),
        num_colors INT
    );
    """)

    # Create Colors_Used table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Colors_Used (
        episode_id INT,
        painting_title VARCHAR(255),
        painting_index INT,
        Black_Gesso INT DEFAULT 0,
        Bright_Red INT DEFAULT 0,
        Burnt_Umber INT DEFAULT 0,
        Cadmium_Yellow INT DEFAULT 0,
        Dark_Sienna INT DEFAULT 0,
        Indian_Red INT DEFAULT 0,
        Indian_Yellow INT DEFAULT 0,
        Liquid_Black INT DEFAULT 0,
        Liquid_Clear INT DEFAULT 0,
        Midnight_Black INT DEFAULT 0,
        Phthalo_Blue INT DEFAULT 0,
        Phthalo_Green INT DEFAULT 0,
        Prussian_Blue INT DEFAULT 0,
        Sap_Green INT DEFAULT 0,
        Titanium_White INT DEFAULT 0,
        Van_Dyke_Brown INT DEFAULT 0,
        Yellow_Ochre INT DEFAULT 0,
        Alizarin_Crimson INT DEFAULT 0,
        FOREIGN KEY (episode_id) REFERENCES Episodes(episode_id),
        PRIMARY KEY (episode_id, painting_title, painting_index)
    );
    """)

    # Create Subject_Matter table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Subject_Matter (
        episode_id INT,
        painting_title VARCHAR(255),
        painting_index INT,
        APPLE_FRAME INT DEFAULT 0,
        AURORA_BOREALIS INT DEFAULT 0,
        BARN INT DEFAULT 0,
        BEACH INT DEFAULT 0,
        BOAT INT DEFAULT 0,
        BRIDGE INT DEFAULT 0,
        BUILDING INT DEFAULT 0,
        BUSHES INT DEFAULT 0,
        CABIN INT DEFAULT 0,
        CACTUS INT DEFAULT 0,
        CIRCLE_FRAME INT DEFAULT 0,
        CIRRUS INT DEFAULT 0,
        CLIFF INT DEFAULT 0,
        CLOUDS INT DEFAULT 0,
        CONIFER INT DEFAULT 0,
        CUMULUS INT DEFAULT 0,
        DECIDUOUS INT DEFAULT 0,
        DIANE_ANDRE INT DEFAULT 0,
        DOCK INT DEFAULT 0,
        DOUBLE_OVAL_FRAME INT DEFAULT 0,
        FARM INT DEFAULT 0,
        FENCE INT DEFAULT 0,
        FIRE INT DEFAULT 0,
        FLORIDA_FRAME INT DEFAULT 0,
        FLOWERS INT DEFAULT 0,
        FOG INT DEFAULT 0,
        FRAMED INT DEFAULT 0,
        GRASS INT DEFAULT 0,
        GUEST INT DEFAULT 0,
        HALF_CIRCLE_FRAME INT DEFAULT 0,
        HALF_OVAL_FRAME INT DEFAULT 0,
        HILLS INT DEFAULT 0,
        LAKE INT DEFAULT 0,
        LAKES INT DEFAULT 0,
        LIGHTHOUSE INT DEFAULT 0,
        MILL INT DEFAULT 0,
        MOON INT DEFAULT 0,
        MOUNTAIN INT DEFAULT 0,
        MOUNTAINS INT DEFAULT 0,
        NIGHT INT DEFAULT 0,
        OCEAN INT DEFAULT 0,
        OVAL_FRAME INT DEFAULT 0,
        PALM_TREES INT DEFAULT 0,
        PATH INT DEFAULT 0,
        PERSON INT DEFAULT 0,
        PORTRAIT INT DEFAULT 0,
        RECTANGLE_3D_FRAME INT DEFAULT 0,
        RECTANGULAR_FRAME INT DEFAULT 0,
        RIVER INT DEFAULT 0,
        ROCKS INT DEFAULT 0,
        SEASHELL_FRAME INT DEFAULT 0,
        SNOW INT DEFAULT 0,
        SNOWY_MOUNTAIN INT DEFAULT 0,
        SPLIT_FRAME INT DEFAULT 0,
        STEVE_ROSS INT DEFAULT 0,
        STRUCTURE INT DEFAULT 0,
        SUN INT DEFAULT 0,
        TOMB_FRAME INT DEFAULT 0,
        TREE INT DEFAULT 0,
        TREES INT DEFAULT 0,
        TRIPLE_FRAME INT DEFAULT 0,
        WATERFALL INT DEFAULT 0,
        WAVES INT DEFAULT 0,
        WINDMILL INT DEFAULT 0,
        WINDOW_FRAME INT DEFAULT 0,
        WINTER INT DEFAULT 0,
        WOOD_FRAMED INT DEFAULT 0,
        FOREIGN KEY (episode_id) REFERENCES Episodes(episode_id),
        PRIMARY KEY (episode_id, painting_title, painting_index)
    );
    """)

def insert_data(file_path):
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        cursor = connection.cursor()

        # Create tables
        create_tables(cursor)

        df = pd.read_csv(file_path)

        # Print the dataframe to ensure it is loaded correctly
        print("DataFrame loaded:")
        print(df.head())
        print("Column names:", df.columns)

        for index, row in df.iterrows():
            # Insert data into Episodes
            episode_sql = """
                INSERT INTO Episodes (
                    painting_title, painting_index, season, episode, date, img_src, youtube_src, num_colors
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            episode_values = (
                row['painting_title'],
                row['painting_index'],
                row['season'],
                row['episode'],
                pd.to_datetime(row['DATE']).strftime('%Y-%m-%d'),
                row['img_src'],
                row['youtube_src'],
                row['num_colors']
            )
            try:
                cursor.execute(episode_sql, episode_values)
                connection.commit()
                episode_id = cursor.lastrowid
                print(f"Inserting data into Episodes: {episode_values}")
            except mysql.connector.Error as err:
                print(f"Episode insertion error: {err}")
                continue  # Skip further processing for this row if there's an error

            # Insert data into Colors_Used
            colors_sql = """
                INSERT INTO Colors_Used (
                    episode_id, painting_title, painting_index, Black_Gesso, Bright_Red, Burnt_Umber, Cadmium_Yellow, Dark_Sienna, 
                    Indian_Red, Indian_Yellow, Liquid_Black, Liquid_Clear, Midnight_Black, Phthalo_Blue, Phthalo_Green, 
                    Prussian_Blue, Sap_Green, Titanium_White, Van_Dyke_Brown, Yellow_Ochre, Alizarin_Crimson
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            colors_values = (
                episode_id,
                row['painting_title'],
                row['painting_index'],
                row.get('Black_Gesso', 0),
                row.get('Bright_Red', 0),
                row.get('Burnt_Umber', 0),
                row.get('Cadmium_Yellow', 0),
                row.get('Dark_Sienna', 0),
                row.get('Indian_Red', 0),
                row.get('Indian_Yellow', 0),
                row.get('Liquid_Black', 0),
                row.get('Liquid_Clear', 0),
                row.get('Midnight_Black', 0),
                row.get('Phthalo_Blue', 0),
                row.get('Phthalo_Green', 0),
                row.get('Prussian_Blue', 0),
                row.get('Sap_Green', 0),
                row.get('Titanium_White', 0),
                row.get('Van_Dyke_Brown', 0),
                row.get('Yellow_Ochre', 0),
                row.get('Alizarin_Crimson', 0)
            )
            try:
                cursor.execute(colors_sql, colors_values)
                connection.commit()
                print(f"Inserting data into Colors_Used: {colors_values}")
            except mysql.connector.Error as err:
                print(f"Colors_Used insertion error: {err}")

            # Insert data into Subject_Matter
            subjects_sql = """
                INSERT INTO Subject_Matter (
                    episode_id, painting_title, painting_index, APPLE_FRAME, AURORA_BOREALIS, BARN, BEACH, BOAT, BRIDGE, BUILDING,
                    BUSHES, CABIN, CACTUS, CIRCLE_FRAME, CIRRUS, CLIFF, CLOUDS, CONIFER, CUMULUS, DECIDUOUS, DIANE_ANDRE, DOCK,
                    DOUBLE_OVAL_FRAME, FARM, FENCE, FIRE, FLORIDA_FRAME, FLOWERS, FOG, FRAMED, GRASS, GUEST, HALF_CIRCLE_FRAME,
                    HALF_OVAL_FRAME, HILLS, LAKE, LAKES, LIGHTHOUSE, MILL, MOON, MOUNTAIN, MOUNTAINS, NIGHT, OCEAN, OVAL_FRAME,
                    PALM_TREES, PATH, PERSON, PORTRAIT, RECTANGLE_3D_FRAME, RECTANGULAR_FRAME, RIVER, ROCKS, SEASHELL_FRAME,
                    SNOW, SNOWY_MOUNTAIN, SPLIT_FRAME, STEVE_ROSS, STRUCTURE, SUN, TOMB_FRAME, TREE, TREES, TRIPLE_FRAME,
                    WATERFALL, WAVES, WINDMILL, WINDOW_FRAME, WINTER, WOOD_FRAMED
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            subjects_values = (
                episode_id,
                row['painting_title'],
                row['painting_index'],
                row.get('APPLE_FRAME', 0),
                row.get('AURORA_BOREALIS', 0),
                row.get('BARN', 0),
                row.get('BEACH', 0),
                row.get('BOAT', 0),
                row.get('BRIDGE', 0),
                row.get('BUILDING', 0),
                row.get('BUSHES', 0),
                row.get('CABIN', 0),
                row.get('CACTUS', 0),
                row.get('CIRCLE_FRAME', 0),
                row.get('CIRRUS', 0),
                row.get('CLIFF', 0),
                row.get('CLOUDS', 0),
                row.get('CONIFER', 0),
                row.get('CUMULUS', 0),
                row.get('DECIDUOUS', 0),
                row.get('DIANE_ANDRE', 0),
                row.get('DOCK', 0),
                row.get('DOUBLE_OVAL_FRAME', 0),
                row.get('FARM', 0),
                row.get('FENCE', 0),
                row.get('FIRE', 0),
                row.get('FLORIDA_FRAME', 0),
                row.get('FLOWERS', 0),
                row.get('FOG', 0),
                row.get('FRAMED', 0),
                row.get('GRASS', 0),
                row.get('GUEST', 0),
                row.get('HALF_CIRCLE_FRAME', 0),
                row.get('HALF_OVAL_FRAME', 0),
                row.get('HILLS', 0),
                row.get('LAKE', 0),
                row.get('LAKES', 0),
                row.get('LIGHTHOUSE', 0),
                row.get('MILL', 0),
                row.get('MOON', 0),
                row.get('MOUNTAIN', 0),
                row.get('MOUNTAINS', 0),
                row.get('NIGHT', 0),
                row.get('OCEAN', 0),
                row.get('OVAL_FRAME', 0),
                row.get('PALM_TREES', 0),
                row.get('PATH', 0),
                row.get('PERSON', 0),
                row.get('PORTRAIT', 0),
                row.get('RECTANGLE_3D_FRAME', 0),
                row.get('RECTANGULAR_FRAME', 0),
                row.get('RIVER', 0),
                row.get('ROCKS', 0),
                row.get('SEASHELL_FRAME', 0),
                row.get('SNOW', 0),
                row.get('SNOWY_MOUNTAIN', 0),
                row.get('SPLIT_FRAME', 0),
                row.get('STEVE_ROSS', 0),
                row.get('STRUCTURE', 0),
                row.get('SUN', 0),
                row.get('TOMB_FRAME', 0),
                row.get('TREE', 0),
                row.get('TREES', 0),
                row.get('TRIPLE_FRAME', 0),
                row.get('WATERFALL', 0),
                row.get('WAVES', 0),
                row.get('WINDMILL', 0),
                row.get('WINDOW_FRAME', 0),
                row.get('WINTER', 0),
                row.get('WOOD_FRAMED', 0)
            )
            try:
                cursor.execute(subjects_sql, subjects_values)
                connection.commit()
                print(f"Inserting data into Subject_Matter: {subjects_values}")
            except mysql.connector.Error as err:
                print(f"Subject_Matter insertion error: {err}")

    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    # Update this path to the correct location of your CSV file
    insert_data('Merged_Output.csv')
