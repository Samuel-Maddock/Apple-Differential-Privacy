
def server_cms(data, sketch_matrix, hash_funcs):
    k,m = sketch_matrix.shape
    n = len(hash_funcs)
    sum = 0
    for i in range (0,k):
        sum += sketch_matrix[i][hash_funcs[i](data)]
    return (m/(m-1))*((1/k)*sum - (n/m))