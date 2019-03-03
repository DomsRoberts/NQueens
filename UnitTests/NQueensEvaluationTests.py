import unittest

from NQueens.NQueensEvaluation import NQueensEvaluation


class NQueensEvaluationTests(unittest.TestCase):

    def test_reflect_x(self):
        evaluation = NQueensEvaluation()
        board = [3,1,4,2,0]
        reflected = evaluation.reflectBoardX(board)
        self.assertEqual(reflected[0], 1)
        self.assertEqual(reflected[1], 3)
        self.assertEqual(reflected[2], 0)
        self.assertEqual(reflected[3], 2)
        self.assertEqual(reflected[4], 4)

    def test_reflect_y(self):
        evaluation = NQueensEvaluation()
        board = [3,1,4,2,0]
        reflected = evaluation.reflectBoardY(board)
        self.assertEqual(reflected[0], 0)
        self.assertEqual(reflected[1], 2)
        self.assertEqual(reflected[2], 4)
        self.assertEqual(reflected[3], 1)
        self.assertEqual(reflected[4], 3)

    def test_rotate_board(self):
        evaluation = NQueensEvaluation()
        board = [3, 1, 4, 2, 0]

        rotated = evaluation.rotateBoard(board)
        self.assertEqual(rotated[0], 2)
        self.assertEqual(rotated[1], 0)
        self.assertEqual(rotated[2], 3)
        self.assertEqual(rotated[3], 1)
        self.assertEqual(rotated[4], 4)