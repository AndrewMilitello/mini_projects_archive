#very simple forward pass I made in Numpy 3 years after watching a Youtube video 
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(0)
data = np.array([[2.9, 1.15, 0.99, 1.22222222], 
               [1.19, 1.55, 0.89, 1.2222]])
labels = np.array([[1, 1, 1, 1], [2, 2, 2, 2]])
class LayerDense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.1*np.random.randn(n_inputs, n_neurons)

        self.biases = np.zeros((1, n_neurons))
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases
    def backward(self, gradient, rate):
        pass        
class rect_linear:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)
def softmax_act(inputs):
    
    exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
    prob = exp_values / np.sum(exp_values, axis=1, keepdims=True)
    return prob
class Loss:
    def calculate(self, output, y):
        sample_losses = self.forward(output, y)
        data_loss = np.mean(sample_losses)
        return data_loss
class loss_CategoricalCrossentropy(Loss):
    def forward(self, y_pred, y_true):
        samples = len(y_pred)
        clipped = np.clip(y_pred, 1e-7, 1-1e-7)
        if len(y_true.shape) == 1:
            confidences = clipped[range(samples), y_true]
        elif len(y_true.shape) == 2:
            confidences = np.sum(clipped*y_true, axis=1) 
        likelioods = -np.log(confidences)
        return likelioods

def gd(lr, x):
    for descent in x:
        deltaoutput = (lr-descent)
        slope = deltaoutput/lr
def sigmoid_derivative(x):
    return x * (1 - x)
    
l1 = LayerDense(4, 16)
l2 = LayerDense(16, 4)
for epoch in range(1):
    l1.forward(data)
    n = softmax_act(l1.output)
    l2.forward(n)

print("Predictions after one forward pass:")
print(l2.output)
loss_function = loss_CategoricalCrossentropy()
loss = loss_function.calculate(l2.output, labels)
adjustments = gd(3, loss * sigmoid_derivative(l2.output))
