import random


def run_ransac(data,calc_coeff, is_inlier,goal_inliers,sample_size, max_iterations, random_seed=None):
    best_ic = 0
    best_model = None
    random.seed(random_seed)
    data = list(data)
    for i in range(max_iterations):
        s = random.sample(data, int(sample_size))
        m = calc_coeff(s)
        ic = 0
        for j in range(len(data)):
            if is_inlier(m, data[j]):
                ic += 1

        if ic > best_ic:
            best_ic = ic
            best_model = m

        if ic >= goal_inliers:
            break

    print('Iterations:' + str(i+1), 'best model:' + str(best_model))
    for j in range(len(data)):
        if is_inlier(m, data[j]):
            (data[j])[2] = -1
    return best_model, best_ic, data