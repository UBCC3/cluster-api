import qcelemental as qcel
import qcengine as qcng
import sys
import json
from util import log_error

root_dir = "."

def format_psi4_single_point(result: dict):
    formatted_result = dict()
    formatted_result["structureInfo"] = {
        1:{
            "visualData":{
                result["molecule"]
            },
            "genericData":{
                "structureId":"default",
                "structureName":"default",
                "method":result["model"]["method"],
                "basisSet":result["model"]["basis"],
                "totalEnergy":result["properties"]["return_energy"],
                "SCF ITERATIONS":result["extras"]["qcvars"]["SCF ITERATIONS"],
                "currentEnergy": result["extras"]["qcvars"]["CURRENT ENERGY"],
                "CURRENT REFERENCE ENERGY":result["extras"]["qcvars"]["CURRENT REFERENCE ENERGY"],
                "DD SOLVATION ENERGY":result["extras"]["qcvars"]["DD SOLVATION ENERGY"],
                "HF KINETIC ENERGY":result["extras"]["qcvars"]["HF KINETIC ENERGY"],
                "HF POTENTIAL ENERGY":result["extras"]["qcvars"]["HF POTENTIAL ENERGY"],
                "HF TOTAL ENERGY":result["extras"]["qcvars"]["HF TOTAL ENERGY"],
                "HF VIRIAL RATIO":result["extras"]["qcvars"]["HF VIRIAL RATIO"],
                "NUCLEAR REPULSION ENERGY":result["extras"]["qcvars"]["NUCLEAR REPULSION ENERGY"],
                "ONE-ELECTRON ENERGY":result["extras"]["qcvars"]["ONE-ELECTRON ENERGY"],
                "TWO-ELECTRON ENERGY":result["extras"]["qcvars"]["TWO-ELECTRON ENERGY"],
                "CURRENT DIPOLE": result["extras"]["qcvars"]["CURRENT DIPOLE"],
                "SCF DIPOLE": result["extras"]["qcvars"]["SCF DIPOLE"]
            },
            "tableData":[
                {
                "tableName": "SCF Total Energies",
                "headers": [
                    {"label":"iteration","span":1,"axis":"y"},
                    {"label":"scf energy","span":1,"axis":"x"}
                ],
                "rows": [],
                "SCF TOTAL ENERGIES": result["extras"]["qcvars"]["SCF TOTAL ENERGIES"]
                }
            ]
        }
    }

    for i in range(int(result["extras"]["qcvars"]["SCF ITERATIONS"])):
        formatted_result["structureInfo"]["1"]["tableData"]["rows"][i+1] = {"id": i, "value": result["extras"]["qcvars"]["SCF TOTAL ENERGIES"][i]}
    return formatted_result
    
def save_to_json(formatted_result: dict, job_name: str):
    with open(job_structure_path + "/" + "result.json", 'w') as file:
        json.dump(formatted_result, file)

def execute_psi4(calculation_type: str, method: str, basis_set: str, job_structure_path: str):
    mol = qcel.models.Molecule.from_file(job_structure_path)

    inp = qcel.models.AtomicInput(
        molecule=mol,
        driver="energy",
        model={"method": method, "basis": basis_set},
        keywords={"scf_type": "df"}
        )

    result = qcng.compute(inp, "psi4",return_dict=True)
    with open(job_structure_path + "/" + job_name + ".out", 'w') as file:
        file.write(str(result))
    return result


if __name__ == "__main__":
    calculation_type = sys.argv[1]
    method = sys.argv[2]
    basis_set = sys.argv[3]
    job_structure_path = sys.argv[4]
    job_name = sys.argv[5]

    match method:
        case "Hartree-Fock":
            method = "hf"
        case "MP2":
            method = "mp2"
        case "DFT":
            method = "b3lyp"
    try:
        result = execute_psi4(calculation_type, method, basis_set, job_structure_path)
        formatted_result = format_psi4_single_point(result)
        save_to_json(formatted_result, job_name)
    except Exception as error:
        raise error