import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

PATH = os.getcwd() + "\\data\\"

def k_mean_clustering(df):
    print(df.head())

    documents = df['processed_title'].values.astype("U")

    vectorizer = TfidfVectorizer()
    features = vectorizer.fit_transform(documents)

    k = 10
    model = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
    model.fit(features)
    
    df['cluster'] = model.labels_

    # output the result to a text file.
    output_file(df)


    print("Cluster centroids: \n")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()

    for i in range(k):
        print("Cluster %d:" % i)
        for j in order_centroids[i, :10]: #print out 10 feature terms of each cluster
            print (' %s' % terms[j])
        print('------------')

def output_file(df):

    clusters = df.groupby('cluster')    

    for cluster in clusters.groups:

        # f = open(PATH + f'processed_clusters\\cluster\\{str(cluster)}.csv', 'w') # create csv file

        data = clusters.get_group(cluster)[['title', 'citations', 'year']] # get title 

        data.to_csv(PATH + f'processed_clusters\\{str(cluster)}.csv')