class RunParameters:

    def __init__(self, dimensions, bounds):
        self.maxIterations = 10000000 #(dimensions * dimensions) * 50
        self.dimensions = dimensions
        self.bounds = bounds
