import numpy as np


class SVMTrainer:

	def __init__ (self, kernel, c):
		self.kernel = kernel
		self._c = c

	def gram_matrix(self, X):
		n_samples, n_features = X.shape
		K = np.zeros((n_samples, n_samples))

		for i, x_i in enumerate(X):
			for j, x_j in enumerate(X):
				K[i, j] = self.kernel(x_i, x_j)
		return K



def main():

	SVM = SVMTrainer(,7)

	X = np.ones((5,5))
	print SVM.gram_matrix(X)


if __name__ == "__main__":
    main()


#TODO: Figure out how to enter Kernel  