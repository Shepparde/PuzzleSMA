import numpy as np

weights = [[100,200,50,600,400,300,500,700],[10,20,5,60,40,30,50,70],[50,70,80,55,67,59,74,90]]

def croisement(population):
	l = len(population[0])//2
	p = np.random.permutation(len(population))
	next_generation = []
	for i in range(0, len(population)//2, 2):
		child_1 = list(population[p[i]][:l])+list(population[p[i+1]][l:])
		child_2 = list(population[p[i+1]][:l])+list(population[p[i]][l:])
		next_generation.append(child_1)
		next_generation.append(child_2)
	return population + next_generation

def mutation(population):
	for i in range(len(population)):
		a = np.random.randint(len(population[i]))
		population[i][a] = 1 if population[i][a]==0 else 0
	return population

def compute_salary(individual):
	return -1*np.sum([bit*weights[0][i] for i,bit in enumerate(individual)])/np.sum(weights[0])

def compute_pub(individual):
	return np.sum([bit*weights[1][i] for i,bit in enumerate(individual)])/np.sum(weights[1])

def compute_weight(individual):
	return -1*np.sum([bit*weights[2][i] for i,bit in enumerate(individual)])/np.sum(weights[2])

def constraint(individual):
	return -compute_weight(individual) < 1000

def selection(population, size):
	limit = size // 3 
	s_sal = sorted(population, key = compute_salary)[:limit]
	s_pub = sorted(population, key = compute_pub)[:limit]
	s_wei = sorted(population, key = compute_weight)[:limit]
	return remove_duplicate(list(filter(constraint,s_sal+s_pub+s_wei)))

def remove_duplicate(pop):
	removed = []
	for i in pop:
		not_in = True
		for j in removed:
			if all([x==y for x,y in zip(i,j)]):
				not_in = False
		if not_in:
			removed.append(i)
	return removed

def alea_pop(size, dim):
	pop = []
	for i in range(size):
		pop.append(np.random.randint(2, size=dim))
	return pop

def VGAstep(pop):
	m_pop = mutation(croisement(pop))
	s_pop = selection(m_pop,size)
	return s_pop

if __name__ == '__main__':
	size = 8
	dim = 8
	nb = 3
	
	pop = alea_pop(size, dim)
	print(len(pop),pop,"\n\n")
	for i in range(nb):
		pop = VGAstep(pop)
	print(len(pop),pop)

