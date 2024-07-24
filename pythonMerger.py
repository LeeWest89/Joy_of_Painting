# import pandas as pd
# from fuzzywuzzy import process, fuzz

# # Read CSV files
# colors_used = pd.read_csv('Colors_Used.csv')
# subject_matter = pd.read_csv('Subject_Matter.csv')
# episode_dates = pd.read_csv('Episode_Dates.csv')

# # Helper function for fuzzy matching
# def fuzzy_merge(df_1, df_2, key1, key2, threshold=85, limit=1):
#     """
#     Fuzzy matching of two DataFrames on a given key.
#     df_1: DataFrame 1
#     df_2: DataFrame 2
#     key1: key column of df_1
#     key2: key column of df_2
#     threshold: matching threshold
#     limit: max number of matches
#     """
#     s = df_2[key2].tolist()
#     matches = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit, scorer=fuzz.token_set_ratio))
    
#     df_1['matches'] = matches
#     df_1['best_match'] = df_1['matches'].apply(lambda x: x[0][0] if x and x[0][1] >= threshold else None)
#     df_1['match_score'] = df_1['matches'].apply(lambda x: x[0][1] if x else 0)
    
#     return df_1.drop(columns=['matches'])

# # Fuzzy merge Colors_Used with Subject_Matter
# colors_used = fuzzy_merge(colors_used, subject_matter, 'painting_title', 'TITLE')

# # Merge with Subject_Matter based on best matches
# merged_df = colors_used.merge(subject_matter, left_on='best_match', right_on='TITLE', how='left', suffixes=('', '_subject'))

# # Fuzzy merge the result with Episode_Dates
# merged_df = fuzzy_merge(merged_df, episode_dates, 'painting_title', 'Episode_TITLE')

# # Merge with Episode_Dates based on best matches
# merged_df = merged_df.merge(episode_dates, left_on='best_match', right_on='Episode_TITLE', how='left', suffixes=('', '_episode'))

# # Drop unnecessary columns, keep Episode_TITLE and drop painting_title
# # merged_df = merged_df.drop(columns=['best_match', 'match_score'])
# columns_to_keep = ['TITLE', 'painting_title', 'Episode_TITLE', 'DATE']
# merged_df = merged_df[columns_to_keep]

# # Save to new CSV
# merged_df.to_csv('Merged_Output.csv', index=False)

import pandas as pd
from fuzzywuzzy import process, fuzz

# Read CSV files
colors_used = pd.read_csv('Colors_Used.csv')
subject_matter = pd.read_csv('Subject_Matter.csv')
episode_dates = pd.read_csv('Episode_Dates.csv')

# Helper function to preprocess titles
def preprocess_title(title):
    return ''.join(title.lower().split())

# Preprocess titles for matching
colors_used['processed_painting_title'] = colors_used['painting_title'].apply(preprocess_title)
subject_matter['processed_TITLE'] = subject_matter['TITLE'].apply(preprocess_title)
episode_dates['processed_Episode_TITLE'] = episode_dates['Episode_TITLE'].apply(preprocess_title)

# Helper function for fuzzy matching with unique matching
def fuzzy_merge(df_1, df_2, key1, key2, processed_key1, processed_key2, threshold=60, limit=1):
    """
    Fuzzy matching of two DataFrames on a given key.
    df_1: DataFrame 1
    df_2: DataFrame 2
    key1: original key column of df_1
    key2: original key column of df_2
    processed_key1: processed key column of df_1
    processed_key2: processed key column of df_2
    threshold: matching threshold
    limit: max number of matches
    """
    s = df_2[processed_key2].tolist()
    matches = df_1[processed_key1].apply(lambda x: process.extract(x, s, limit=limit, scorer=fuzz.token_set_ratio))
    
    df_1['matches'] = matches
    df_1['best_match'] = df_1['matches'].apply(lambda x: df_2.iloc[s.index(x[0][0])][key2] if x and x[0][1] >= threshold else None)
    df_1['match_score'] = df_1['matches'].apply(lambda x: x[0][1] if x else 0)
    
    return df_1.drop(columns=['matches'])

# Function to merge DataFrames uniquely
def unique_merge(df_1, df_2, key1, key2, processed_key1, processed_key2):
    """
    Merge two DataFrames uniquely based on best fuzzy matches.
    """
    # Fuzzy merge
    df_1 = fuzzy_merge(df_1, df_2, key1, key2, processed_key1, processed_key2)
    
    # Merge based on best matches
    merged_df = df_1.merge(df_2, left_on='best_match', right_on=key2, how='left', suffixes=('', '_subject'))
    
    # Drop intermediate columns
    merged_df = merged_df.drop(columns=['best_match', 'match_score'])
    
    return merged_df

# Merge Colors_Used with Subject_Matter uniquely
merged_df = unique_merge(colors_used, subject_matter, 'painting_title', 'TITLE', 'processed_painting_title', 'processed_TITLE')

# Ensure processed columns are present
merged_df['processed_painting_title'] = merged_df['painting_title'].apply(preprocess_title)
episode_dates['processed_Episode_TITLE'] = episode_dates['Episode_TITLE'].apply(preprocess_title)

# Merge the result with Episode_Dates uniquely
merged_df = unique_merge(merged_df, episode_dates, 'painting_title', 'Episode_TITLE', 'processed_painting_title', 'processed_Episode_TITLE')

# Keep only one entry per season for each title
def filter_season_duplicates(df, key_col, season_col):
    """
    Filter out duplicate entries for each title by keeping only one entry per season.
    """
    # Remove exact duplicates first
    df = df.drop_duplicates(subset=[key_col, season_col])
    
    # Keep one entry per title per season
    df_filtered = df.groupby([key_col, season_col], as_index=False).first()
    
    return df_filtered

# Apply the filter
merged_df = filter_season_duplicates(merged_df, 'painting_title', 'season')

# Sort by season and episode
merged_df = merged_df.sort_values(by=['season', 'episode']).reset_index(drop=True)

# # Generate IDs based on the sorted order
merged_df.insert(0, '', range(1, len(merged_df) + 1))

# Drop specific unnecessary columns
columns_to_drop = ['processed_painting_title', 'processed_TITLE', 'processed_Episode_TITLE']  # Add columns to drop if needed
merged_df = merged_df.drop(columns=columns_to_drop, errors='ignore')

# Save to new CSV
merged_df.to_csv('Merged_Output.csv', index=False, header=True)

print("Merged CSV with all relevant data created successfully.")
