import pandas

if __name__ == '__main__':
    df = pandas.read_json('web-scraping/shows-4.json')
    filtered = df[df['rating'] > 0]
    grouped = filtered.groupby('name')
    popular = grouped.filter(lambda ratings: len(ratings) > 10)
    sorted_df = popular.groupby('name').mean().sort_values('rating', ascending=False)