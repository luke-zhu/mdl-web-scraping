import pandas

if __name__ == '__main__':
    df = pandas.read_json('web-scraping/ratings-1.json')
    scores = df[['title', 'score']]
    filtered = scores[scores.score > 0]
    grouped = filtered.groupby('title')

    aggs = {
        'score': {
            'average_score': 'mean',
            'num_scores': 'count'
        }
    }
    transformed = grouped.agg(aggs)
    sorted_df = transformed.score[transformed.score.num_scores > 25] \
        .sort_values('average_score', ascending=False)
    sorted_df.to_json('top-shows-2.json')