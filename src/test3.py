"""
DO NOT EDIT THIS FILE !!!
"""
import unittest

from seminar3 import *
from src.test_utils import check_layer_gradient, get_preprocessed_data, check_model_gradient


class TestRelu(unittest.TestCase):
    """1 point"""
    def testForward(self):
        x = np.array([[-1, 2, 3],
                      [1, -2, 0.1]
                      ])
        expected = np.array([[0, 2, 3], [1, 0, 0.1]])
        relu = ReLULayer()
        self.assertTrue(np.array_equal(relu.forward(x), expected))

    def testBackward(self):
        x = np.array([[-1, 2, 3],
                      [1, -2, 0.1]
                      ])
        result = check_layer_gradient(ReLULayer(), x)
        self.assertTrue(result)


class TestFullyConnected(unittest.TestCase):
    """1 point"""
    def testForward(self):
        n_input, n_output = 3, 2
        fc_layer = DenseLayer(n_input, n_output)
        fc_layer.W = Param(np.ones((n_input, n_output)))
        fc_layer.B = Param(np.ones((1, n_output)))
        x = np.ones((1, 3))
        expected = np.ones((1, 2)) * 4
        result = fc_layer.forward(x)
        self.assertTrue(np.array_equal(result, expected))

    def testBackward(self):
        n_input, n_output = 3, 2
        fc_layer = DenseLayer(n_input, n_output)
        x = np.array([[-1, 2, 3],
                      [1, -2, 0.1]
                      ])
        self.assertTrue(check_layer_gradient(fc_layer, x))


class TestNetGradients(unittest.TestCase):
    """1 point"""
    def setUp(self) -> None:
        n_samples, self.n_dims = 32, 128
        self.X = np.random.uniform(-1, 1, size=(n_samples, self.n_dims))
        self.y = np.random.randint(0, 10, size=n_samples)

    def testComputeLossAndGrad(self):
        neural_net = TwoLayerNet(n_input=self.n_dims, n_output=10, hidden_layer_size=16)
        neural_net.forward(self.X, self.y)
        self.assertLess(neural_net.loss, 3.0)
        self.assertGreater(neural_net.loss, 2.0)

    def testWithoutReg(self):
        neural_net = TwoLayerNet(n_input=self.n_dims, n_output=10, hidden_layer_size=16, reg=0.0)
        result = check_model_gradient(neural_net, self.X, self.y, tol=1e-1)
        self.assertTrue(result)

    def testWithReg(self):
        model_with_reg = TwoLayerNet(n_input=self.n_dims, n_output=10, hidden_layer_size=16, reg=100)
        result = check_model_gradient(model_with_reg, self.X, self.y, tol=1e-1)
        self.assertTrue(result)


class TestModelOverFitting(unittest.TestCase):
    """1 point"""
    def testOverFitting(self):
        N_samples = 32
        (x_train, y_train), _ = get_preprocessed_data(include_bias=False)
        dev_idx = np.random.choice(len(x_train), N_samples)
        X_dev, y_dev = x_train[dev_idx], y_train[dev_idx]
        n_input, n_out, hidden_size = 3072, 10, 128
        net = TwoLayerNet(n_input, n_out, hidden_size)

        loss_history = net.fit(X_dev, y_dev,
                               learning_rate=5e-3, num_iters=1000,
                               batch_size=N_samples, verbose=True)
        self.assertLess(loss_history[-1], 1.0)
        self.assertGreater(loss_history[-1], 0.0)


if __name__ == '__main__':
    unittest.main()