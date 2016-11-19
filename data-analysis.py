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

    pairs = pd.merge(filtered[['user', 'title']], filtered[['user', 'title']],
        how='inner',
        on=['user'])

    pair_counts= pairs.groupby(['title_x', 'title_y']).count()
    """
    for title1, group1 in grouped:
        print(title1)
        num_t1 = len(group1)
        for title2, group2 in grouped:
            num_t2 = len(group2)
            num_both = len(pd.merge(group1, group2, how='inner', on=['user']))
            show_similarity[title1][title2] = num_both ** 2 / (num_t1 * num_t2)
            # print('{}, {}'.format(title1, title2))
    """

    show_similarity.to_json('show-similarity-1.json')