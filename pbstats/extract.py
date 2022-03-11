import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist

DEBUG_flowers = 0
DEBUG_visits = 0
DEBUG_combine = 0
DEBUG_stats = 0

def extract_data(rawData):
    flowerData = rawData['data']['0']
    flowerRows = []

    for item in flowerData:
        if item['id'][0] == 'F':
            flowerID = item['id']
            time = item['time']
            frame = item['frame']
            cx = item['cx']
            cy = item['cy']

            flowerRows.append([flowerID, time, frame, cx, cy])

            if DEBUG_flowers == 1:
                print(item)
                print()

    flower_df = pd.DataFrame(flowerRows, columns=['Flower', 'Time', 'Frame', 'f_cx', 'f_cy'])

    visitData = rawData['data']
    visitRows = []

    for item in visitData.items():
        if item[1]:
            visitlabel = item[0]
            visitInfo = item[1][0]
            pollinatorID = visitInfo['id']
            if pollinatorID[0] == 'P':
                time = visitInfo['time']
                frame = visitInfo['frame']
                cx = visitInfo['cx']
                cy = visitInfo['cy']
                visitDuration = (visitInfo['span']['f2'] - visitInfo['span'][
                    'f1']) / 20 if 'span' in visitInfo else np.nan

                visitRows.append([pollinatorID, time, frame, cx, cy, visitDuration])

                if DEBUG_visits == 1:
                    print(visitlabel)
                    print(visitInfo)
                    print()

    visit_df = pd.DataFrame(visitRows, columns=['Pollinator', 'Time', 'Frame', 'p_cx', 'p_cy', 'Visit Duration (s)'])

    flower_coordinates = flower_df.loc[:, ['f_cx', 'f_cy']]
    pollinator_coordinates = visit_df.loc[:, ['p_cx', 'p_cy']]

    if DEBUG_combine == 1:
        print(flower_coordinates)
        print(pollinator_coordinates)

    dists = cdist(pollinator_coordinates, flower_coordinates)

    mindist, flowerIdx = np.min(dists, axis=1), np.argmin(dists, axis=1)

    flowers = flower_df.loc[flowerIdx, ['Flower']]
    flower_cx = flower_df.loc[flowerIdx, ['f_cx']]
    flower_cy = flower_df.loc[flowerIdx, ['f_cy']]

    if DEBUG_combine == 1:
        print(mindist)
        print(flowerIdx)
        print(flowers)
        print(flower_cx)
        print(flower_cy)

    augmented_visit_df = visit_df
    augmented_visit_df['Distance'] = mindist
    augmented_visit_df['Flower'] = flowers['Flower'].values
    augmented_visit_df['f_cx'] = flower_cx['f_cx'].values
    augmented_visit_df['f_cy'] = flower_cy['f_cy'].values

    augmented_visit_df.columns

    invalid_data = augmented_visit_df.loc[np.isnan(augmented_visit_df["Visit Duration (s)"])]

    if not invalid_data.empty:
        display(invalid_data)
        print("Warning: Some data is invalid")

    return augmented_visit_df
