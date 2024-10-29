from unittest import TestCase
from pocket_cube_solver import *
import unittest
from utils.timeout import timeout
from gradescope_utils.autograder_utils.decorators import weight, visibility, number

class TestsOfStarterCode(TestCase):
    def test_rotations(self):
        #Check that each rotation has order 4.
        #This is a basic assurance that the move permutations were written correctly.
        P = pocket_cube()
        Q = pocket_cube()
        for mv in pocket_cube.move_permutation_dict:
            for i in range(4):
                P.perform_move(mv,mutate=True)
            assert P==Q 
    def test_scramble_unscramble(self):
        #Check that scrambling, then performing the reverse moves unscrambles the cube.
        #This is a basic assurance that move sequences are being inverted correctly.
        P=pocket_cube()
        scramble_sequence = P.scramble()
        assert not P.state == list(range(24)) #This may occasionally fail if we scramble back to identity. But this is rare.
        unscramble_sequence= pocket_cube.invert_move_sequence(scramble_sequence)
        P.perform_move_sequence(unscramble_sequence)
        assert P.state == list(range(24))

    def test_twist_invariant(self):
        #Checks that the total twist is always 0.
        P=pocket_cube()
        for mv in pocket_cube.move_cost_dict:
            Q = P.perform_move(mv)
            total_twist = 0
            for cubie in itertools.product([0,1],repeat = 3):
                total_twist += Q.get_twist_of_cubie(cubie)
            assert total_twist%3==0

class TestsOfStudentCode(TestCase):
    small_scrambles = [['F'],['U2'],['F','B'],['Bp','U','R2','Dp','L'], ['R','L','U','R','D'],['Dp','Up','R','B2','Lp']]
    @weight(5)
    @timeout(120)
    def test_small_scramble_BFS(self):
        scrambled_cube =pocket_cube()
        for scramble_seq in type(self).small_scrambles:
            scrambled_cube.perform_move_sequence(scramble_seq)
            assert not scrambled_cube == pocket_cube()
            move_sequence = solve_cube(scrambled_cube, method = "BFS")
            scrambled_cube.perform_move_sequence(move_sequence)
            assert scrambled_cube==pocket_cube()
    @weight(5)
    @timeout(120)#This stops you from taking more than 2 minutes.
    def test_small_scramble_dijkstra(self):
        scrambled_cube =pocket_cube()
        for scramble_seq in type(self).small_scrambles:
            scrambled_cube.perform_move_sequence(scramble_seq, mutate=True)
            assert not scrambled_cube == pocket_cube()
            move_sequence = solve_cube(scrambled_cube, method = "dijkstra")
            scrambled_cube.perform_move_sequence(move_sequence)
            assert scrambled_cube==pocket_cube()
    @weight(5)
    @timeout(120)#This stops you from taking more than 2 minutes.
    def test_bfs_dijkstra_path_costs(self):
        #This checks that for the half turn metric, the costs from dijkstra's algorithm and bfs are the same.
        #Note that the paths may not be the same.
        #You may re-write this test to agree with the function as you wrote them in pocket_cube_solver.py
        pocket_cube.change_cost_type("QTM")
        for scramble_seq in type(self).small_scrambles:
            scrambled_cube = pocket_cube()
            scrambled_cube.perform_move_sequence(scramble_seq)
            _, dijkstra_record = dijkstra(scrambled_cube, condition = lambda cube: cube.state == list(range(24)), get_neighbors=lambda cube: cube.get_half_neighbors())
            _, bfs_record = BFS(scrambled_cube, condition = lambda cube: cube.state == list(range(24)), get_neighbors=lambda cube: cube.get_half_neighbors())
            for key in [key for key in dijkstra_record if key in bfs_record]:
                dijkstra_path= get_path_from_search(scrambled_cube,key, dijkstra_record)
                bfs_path = get_path_from_search(scrambled_cube,key, bfs_record)
                assert pocket_cube.move_sequence_cost(bfs_path)==pocket_cube.move_sequence_cost(dijkstra_path)
        pocket_cube.change_cost_type("ALT")
if __name__=="__main__":
    #T = TestsOfStudentCode()
    #T.test_small_scramble_dijkstra()
    unittest.main()