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
    
    users = filtered.groupby('user')
    """
    pairs = pd.merge(filtered[['user', 'title']],
        filtered[['user', 'title']],
        how='inner',
        on=['user'])

    def jaccard(group):
        union_size = len(sorted_df.loc[group.title_x]['num_scores']) + \
            len(sorted_df.loc[group.title_y]['num_scores']) - \
            group.count()
        return group['user'].count() / union_size

    similarities = pairs.groupby(['title_x', 'title_y']).apply(jaccard)
    """
    """
    for i in range(0, 81):
        print(i)
        pair_counts = pd.read_csv('pair-counts/pair-counts-{}'.format(i))
        similarities = pair_counts.apply(
            lambda row: row['user'] / \
                (sorted_df.loc[row.title_x]['num_scores'] + \
                sorted_df.loc[row.title_y]['num_scores'] - \
                row['user']),
            axis=1)
        similarities.to_csv('similarities/similarities-{}.csv'.format(i))
    """
    """
    for i in range(0, 81):
        print(i)
        pair_counts = pd.read_csv('pair-counts/pair-counts-{}'.format(i))
        similarities = pd.read_csv('similarities/similarities-{}.csv'.format(i),
            header=None)
        final_df = pair_counts.join(similarities) \
            .set_index(['title_x', 'title_y']) \
            .rename(columns={'user': 'count', 1: 'similarity'}) \
            .drop([0], axis=1)
        final_df.to_csv('final-dfs/final-df-{}.csv'.format(i))
    """
