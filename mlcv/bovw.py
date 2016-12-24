import numpy as np
import sklearn.cluster as cluster

import mlcv.input_output as io


def create_codebook(X, k=512, codebook_name=None, k_means_init='random'):
    batch_size = 20*k if X.shape[0] > 20*k else X.shape[0] / 10
    codebook = cluster.MiniBatchKMeans(n_clusters=k, verbose=False, batch_size=batch_size, compute_labels=False,
                                       reassignment_ratio=10 ** -4, init=k_means_init)

    if codebook_name is not None:
        # Try to load a previously trained codebook
        try:
            codebook = io.load_object(codebook_name)
        except (IOError, EOFError):
            codebook.fit(X)
            # Store the model with the provided name
            io.save_object(codebook, codebook_name)
    else:
        codebook.fit(X)

    return codebook


def visual_words(X, y, descriptors_indices, codebook):
    k = codebook.cluster_centers_.shape[0]
    prediction = codebook.predict(X)
    v_words = [np.bincount(prediction[descriptors_indices == i], minlength=k) for i in
               range(0, descriptors_indices.max() + 1)]
    labels = [y[descriptors_indices == i][0] for i in
              range(0, descriptors_indices.max() + 1)]
    return np.array(v_words, dtype=np.float64), np.array(labels)
