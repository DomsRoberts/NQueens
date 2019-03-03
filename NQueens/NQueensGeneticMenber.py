from Framework.Members.GeneticMember import GeneticMember


class NQueensGeneticMember(GeneticMember):

    def __init__(self, parameter, startLocation, mutation_count):
        super(NQueensGeneticMember, self).__init__(parameter, startLocation, mutation_count)
        self.success_count = 0

    def evaluate(self, evaluator):
        result = super(NQueensGeneticMember, self).evaluate(evaluator)

        if result == 0:
            self.success_count += 1