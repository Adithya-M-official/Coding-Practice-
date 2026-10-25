import numpy as np

learning_rate = 0.09

def relu(input, derivative = False, leaky_relu = True):
    if derivative:
        if leaky_relu:
            return np.where(input > 0, 1.0, learning_rate)
        else:
            return np.where(input > 0, 1.0, 0)
    if leaky_relu:
        return np.where(input > 0, input, input*learning_rate)
    else:
        return np.where(input > 0, input, 0)

def sigmoid(input, derivative = False):
    if derivative:
        sigmoid_matrix = sigmoid(input, derivative = False)
        return sigmoid_matrix*(1-sigmoid_matrix)
    else:
        return (1/(1+np.exp(-input)))

        
class Layer:
    #makes a layer object that stores inout matrix and neuron count for that layer
    #handles mathematical expressions related to forward pass and backpropagation of values between layers.
    def __init__(self, inputs, neuron_count):
        inputs = np.array(inputs)
        
        if inputs.ndim == 1:
            self.input_matrix = inputs.reshape(-1,1)
        else:
            self.input_matrix = inputs
        self.neuron_count = neuron_count

        self.weights = self.initialise_weights()
        self.biases = self.initialise_biases()

    def initialise_weights(self):
        #initialises weight matrix based on input size and number of neurons
        weights = np.random.randn(self.neuron_count, self.input_matrix.shape[0])
        return weights
        
    def initialise_biases(self):
        #initialises bias matrix based on neuron count
        biases = np.zeros((self.neuron_count,1))
        return biases

    def forward(self):
        # does a forward pass based on initialised weights, biases and inputs
        # uses eqn y = wa+b, w is weights, a is inputs, b is bias
        # returns the activated y value, to be passed as input matrix to the next layer
        output = (self.weights @ self.input_matrix) + self.biases
        activated_outputs = relu(output)
        return activated_outputs

    def backward(self, error_vector, next_layer_weights):
        # calculates raw outputs for current layer
        output = (self.weights @ self.input_matrix)+self.biases

        # uses eqn, gradient =  [ W(l+1) @ delta(l+1) ] @ a(l-1)
        # the dot product of incoming activated inputs from previous layer with the dot product of transpose of weight matrix of current layer and error vector of next layer is taken
        new_error_vector = (next_layer_weights.T @ error_vector) * relu(output, derivative = True)
        
        error_gradient = new_error_vector @ self.input_matrix.T

        # error gradient is subtracted from current weight matrix
        # this process is gradient descend
        # it pushes the values of weight matrix toward a local minima
        self.weights -= (learning_rate * error_gradient)
        self.biases -= (learning_rate * new_error_vector)
        return new_error_vector, self.weights
        
    def calc_error(self, desired_output):
        # calculates output of the layer, within the layer itself
        # uses the inputs from the previous layer and calculates wa+b
        
        output = (self.weights @ self.input_matrix) + self.biases
        
        # passes the output through relu
        activated_outputs = sigmoid(output)

        # calculates loss and error vectors
        # loss = (y'-y)^2
        # error vector = 2(y'-y) * sigmoid_derivative(z), z is the unactivated output of the output layer
        loss = np.sum((activated_outputs - desired_output) ** 2)
        error_vector = 2 * (activated_outputs - desired_output) * sigmoid(output, derivative = True)

        self.biases -= (learning_rate*error_vector)
        return error_vector, self.weights, loss

    def get_predictions(self, inputs):
        print(self.weights.shape, inputs.shape, sep=" | ")
        output = (self.weights @ inputs) + self.biases
        return sigmoid(output)
        
class NeuralNetwork:
    def __init__(self):
        self.layers = []

    def add_layer(self,*layer_objs):
        for layer_obj in layer_objs:
            self.layers.append(layer_obj)

    def train(self, inputs, outputs, epochs):
        for epoch in range(epochs):
            totalloss = 0
            for idx in range (len(inputs)):
                self.layers[0].input_matrix = inputs[idx].reshape(-1,1)
                desired_output = outputs[idx].reshape(-1,1)

                current_inputs = self.layers[0].input_matrix
                for layer in self.layers:
                    layer.input_matrix = current_inputs
                    current_inputs = layer.forward()
                
                for layer in self.layers[ : : -1]:
                    if self.layers.index(layer) == len(self.layers)-1:
                        error_vector, next_weights, loss = layer.calc_error(desired_output)
                        totalloss += loss
                    else:    
                        error_vector, next_weights = layer.backward(error_vector, next_weights)
            
            

    def test(self, inputs, outputs):
        for idx in range (len(inputs)):
            current_inputs = inputs[idx].reshape(-1,1)
            predictions = None
            for layer in self.layers:
                if self.layers.index(layer) != len(self.layers) - 1:
                    layer.input_matrix = current_inputs
                    current_inputs = layer.forward()
                else:
                    predictions = layer.get_predictions(current_inputs)

            prediction = predictions[0, 0]
            target = outputs[idx][0, 0]
            
            print(f"input : {current_inputs} | target : {target} | prediction : {prediction}")
                    
if __name__ == '__main__':
    nn = NeuralNetwork()
    inputs = np.array([[[0], [0]], [[0], [1]], [[1], [0]], [[1], [1]]])
    outputs = np.array([[[0]], [[1]], [[1]], [[0]]])

    input_mtx = np.array([[0], [1]])
    layer1 = Layer(input_mtx, 2)
    layer2 = Layer(layer1.forward(), 4)
    layer3 = Layer(layer2.forward(), 3)
    layer4 = Layer(layer3.forward(), 1)
    nn.add_layer(layer1, layer2, layer3, layer4)
    
    desired_output = np.array([[1]])

    nn.train(inputs, outputs, epochs = 20000)
    nn.test(inputs, outputs)

