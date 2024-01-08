import unittest
import json
import platform

import os

import numpy as np
import wildmeshing as wm

# import igl
# import meshplot as mp
# mp.offline()


class TetrahedralizeTest(unittest.TestCase):
    def test_doc(self):
        print(wm.tetrahedralize.__doc__)

    def test_run(self):
        root_folder = os.path.join("..", "data")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        mesh_path = os.path.join(dir_path, root_folder, "small.stl")

        wm.tetrahedralize(mesh_path, "tet_test.msh",
                          mute_log=True, stop_quality=1000)

    def test_data(self):
        root_folder = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "..", "data")
        V = np.load(os.path.join(root_folder, "V.npy"))
        F = np.load(os.path.join(root_folder, "F.npy"))

        tetra = wm.Tetrahedralizer(stop_quality=1000)
        tetra.set_mesh(V, F)
        tetra.tetrahedralize()
        VT, TT, _ = tetra.get_tet_mesh()
        # mp.plot(VT, TT, filename="plot.html")

    def test_boolean(self):
        if platform.system() == "Windows":
            return

        root_folder = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "..", "data")

        csg_tree = {
            "operation": "difference",
            "left": {
                "operation": "intersection",
                "left": os.path.join(root_folder, "csg_input", "box.stl"),
                "right": os.path.join(root_folder, "csg_input", "ball.stl")
            },
            "right": {
                "operation": "union",
                "left": os.path.join(root_folder, "csg_input", "x.stl"),
                "right": {
                    "operation": "union",
                    "left": os.path.join(root_folder, "csg_input", "y.stl"),
                    "right": os.path.join(root_folder, "csg_input", "z.stl")
                }
            }
        }

        wm.boolean_operation(json.dumps(csg_tree), "bool", stop_quality=1000)

    def test_boolean1(self):
        if platform.system() == "Windows":
            return

        root_folder = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "..", "data")

        csg_tree = {
            "operation": "difference",
            "left": {
                "operation": "intersection",
                "left": os.path.join(root_folder, "csg_input", "box.stl"),
                "right": os.path.join(root_folder, "csg_input", "ball.stl")
            },
            "right": {
                "operation": "union",
                "left": os.path.join(root_folder, "csg_input", "x.stl"),
                "right": {
                    "operation": "union",
                    "left": os.path.join(root_folder, "csg_input", "y.stl"),
                    "right": os.path.join(root_folder, "csg_input", "z.stl")
                }
            }
        }

        tetra = wm.Tetrahedralizer(stop_quality=1000)
        tetra.load_csg_tree(json.dumps(csg_tree))
        tetra.tetrahedralize()
        VT, TT, _ = tetra.get_tet_mesh()

        # mp.plot(VT, TT, filename="plot.html")


if __name__ == '__main__':
    unittest.main()
