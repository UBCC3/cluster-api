import qcelemental as qcel
import qcengine as qcng
import sys

def execute_psi4(calculation_type, method, basis_set, job_structure):
    mol = qcel.models.Molecule.from_data(job_structure)

    inp = qcel.models.AtomicInput(
        molecule=mol,
        driver="energy",
        model={"method": method, "basis": basis_set},
        keywords={"scf_type": "df"}
        )

    ret = qcng.compute(inp, "psi4",return_dict=True)

    print(ret)

if __name__ == "__main__":
    calculation_type = sys.argv[1]
    method = sys.argv[2]
    basis_set = sys.argv[3]
    job_structure = sys.argv[4]
    execute_psi4(calculation_type, method, basis_set, job_structure)