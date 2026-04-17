import pandas as pd
import club_rec_recsys as rec_sys
import ast

df = pd.read_csv('data/clubs_with_interest_areas.csv')
df['interest_areas_ids'] = df['interest_areas_ids'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

def interest_scoring(user_interests, club_interests):
    if (len(user_interests) == 0):
        return 1
    user_interests.sort()
    club_interests.sort()
    i = j = count = 0
    while i < len(user_interests) and j < len(club_interests):
        if user_interests[i] == club_interests[j]:
            count += 1
            i += 1
            j += 1
        elif user_interests[i] < club_interests[j]:
            i += 1
        else:
            j += 1
    return count/len(user_interests)

scoring_results = []

def top_5(user_text, user_interests):
    df_cos = rec_sys.get_sim_score(user_text)

    scoring_results = []

    cos_map = dict(zip(df_cos['id'], df_cos['sim_score']))

    for row in df.itertuples():
        each_club = {}
        sim_score = cos_map.get(row.id, 0.0)
        interest_match = interest_scoring(user_interests, row.interest_areas_ids)
        each_club["id"] = row.id
        each_club["cos_score"] = float(sim_score)
        each_club['interest_match'] = float(interest_match)
        each_club['total'] = float(sim_score * 0.7 + interest_match * 0.3)

        scoring_results.append(each_club)

    return sorted(scoring_results, key=lambda x: x['total'], reverse=True)[:5]

dd = top_5("i want to became a data scientist and develop my CV and find new connectins", [3, 6])

for i in dd:
    print(i["id"], i["total"])