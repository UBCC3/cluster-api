import qcelemental as qcel
import qcengine as qcng
import sys

def execute_psi4(calculation_type, method, basisSet):
    mol = qcel.models.Molecule.from_data("""
    O  0.0  0.000  -0.129
    H  0.0 -1.494  1.027
    H  0.0  1.494  1.027
    """)

    inp = qcel.models.AtomicInput(
        molecule=mol,
        driver="energy",
        model={"method": method, "basis": basisSet},
        keywords={"scf_type": "df"}
        )

    ret = qcng.compute(inp, "psi4",return_dict=True)

    print(ret)

if __name__ == "__main__":
    execute_psi4(sys.argv[1], sys.argv[2], sys.argv[3])