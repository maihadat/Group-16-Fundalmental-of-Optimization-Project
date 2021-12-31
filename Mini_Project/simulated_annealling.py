import CPusingortools as cp
import branch_and_bound as bnb
from numpy import exp
import random as rd

# objective function
def objective(x,filename):
    N, M, m, d, s, e = cp.input(filename)
    x_eval = [0]*max(e)
    for i in range(N):
        for j in range(1, max(e)+1):
            if x[i] == j:
                x_eval[j-1] += d[i]
    return x_eval, max(x_eval) - bnb.min_diff_zero(x_eval)

# simulated annealing algorithm
def simulated_annealing(objective, n_iterations, temp, filename):
    N, M, m, d, s, e = cp.input(filename)
    # generate an initial point
    best = [rd.randint(s[i], e[i]) for i in range(N)]
    # evaluate the initial point
    best_eval = objective(best,filename)[1]
    print(best)
	# current working solution
    curr, curr_eval = best, best_eval
    solution = list()
	# run the algorithm
    for i in range(n_iterations):
        # take a step
        candidate = [rd.randint(s[i], e[i]) for i in range(N)]
		# evaluate candidate point
        candidate_eval = objective(candidate,filename)[1]
		# check for new best solution
        if candidate_eval < best_eval:
			# store new best point
            best, best_eval = candidate, candidate_eval
			# keep track of scores
            if max(objective(best,filename)[0]) < M + 1 and bnb.min_diff_zero(objective(best,filename)[0]) > m - 1:
                solution.append((best, objective(best,filename)[0], best_eval))
			# report progress
            print('>%d f(%s, %s) = %.5f' % (i, best, objective(best,filename)[0], best_eval))
		# difference between candidate and current point evaluation
        diff = candidate_eval - curr_eval
		# calculate temperature for current epoch
        t = temp / float(i + 1)
		# calculate metropolis acceptance criterion
        metropolis = exp(-diff / t)
		# check if we should keep the new point
        if (diff < 0 or rd.random() < metropolis):
            # store the new current point
            curr, curr_eval = candidate, candidate_eval
    return [best, best_eval, solution]

if __name__ == '__main__':
    filename = 'MyData/data9.txt'
    # define the total iterations
    n_iterations = 1000
    # initial temperature
    temp = 100
    # perform the simulated annealing search
    best, score, solution = simulated_annealing(objective, n_iterations, temp, filename)
    print('Done!')
    print(solution[-1])


