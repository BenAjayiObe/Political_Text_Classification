import numpy as np
import kernel
import cvxopt


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


	def _compute_multipliers(self, X, y):
		n_samples, n_features = X.shape

		K = self.gram_matrix(X)
		# Solves
		# min 1/2 x^T P x + q^T x
		# s.t.
		#  Gx \coneleq h
		#  Ax = b

		P = cvxopt.matrix(np.outer(y, y) * K)
		q = cvxopt.matrix(-1 * np.ones(n_samples))

		# -a_i \leq 0
		# TODO(tulloch) - modify G, h so that we have a soft-margin classifier
		G_std = cvxopt.matrix(np.diag(np.ones(n_samples) * -1))
		h_std = cvxopt.matrix(np.zeros(n_samples))

		# a_i \leq c
		G_slack = cvxopt.matrix(np.diag(np.ones(n_samples)))
		h_slack = cvxopt.matrix(np.ones(n_samples) * self._c)

		G = cvxopt.matrix(np.vstack((G_std, G_slack)))
		h = cvxopt.matrix(np.vstack((h_std, h_slack)))

		A = cvxopt.matrix(y, (1, n_samples))
		#A = cvxopt.matrix(np.diag(np.ones(y)))
		b = cvxopt.matrix(0.0)

		solution = cvxopt.solvers.qp(P, q, G, h, A, b)

		# Lagrange multipliers
		return np.ravel(solution['x'])


def main():

	SVM = SVMTrainer(kernel.Kernel.linear(),7)

	X = np.ones((5,5))
	print SVM.gram_matrix(X)
	Y = np.ones((5,5))
	print SVM._compute_multipliers(Y,5)


if __name__ == "__main__":
    main()


#TODO: Figure out how to enter Kernel  