import numpy as np
import pandas as pd

if __name__ == '__main__':
    df = pd.read_json('web-scraping/ratings-1.json')
    filtered = df[df['score'] > 0] \
        .groupby('title') \
        .filter(lambda show: show.user.unique().size > 25)
    grouped = filtered.groupby('title')

    aggs = {
        'score': {
            'average_score': 'mean',
            'num_scores': 'count', # also equal to # users
        },
    }
    sorted_df = grouped.agg(aggs).score \
        .sort_values('average_score', ascending=False)

    # Get P(A and B)/P(A)/P(B) for each pair of shows (A, B)
    
    users = filtered.groupby('user')

    show_similarity = pd.DataFrame(index=sorted_df.index,
        columns=sorted_df.index)

    
    for show1 in sorted_df.index:
        for show2 in sorted_df.index:
            x = filtered[filtered['title'] == show1]
            y = filtered[filtered['title'] == show2]
            x_and_y = pd.merge(x, y, how='inner', on=['user'])
            show_similarity[show1][show2] = len(x_and_y) / np.sqrt(len(x) * len(y))
    
    show_similarity.to_json('show-similarity-1.json')
