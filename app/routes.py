from flask import url_for, render_template, redirect, session
from rdkit import Chem
import requests

from app import app
from app.forms import MolForm, Result

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MolForm()
    if form.validate_on_submit():
        result = read_input(form.value.data, form.choices.data)
        session['result'] = result._asdict() if result else None
        return redirect(url_for('result'))
    return render_template('index.html', title='Home', form=form)

@app.route('/result')
def result():
    result = session.get('result')
    return render_template('result.html', title='Result', result=result)

# Helper functions
def read_input(value, choice):
    try:
        print(choice)
        if choice == 'smiles':
            mol = smi_to_mol(value)
        elif choice == 'inchi':
            mol = inchi_to_mol(value)
        elif choice == 'inchikey':
            mol = inchikey_to_mol(value)
        elif choice == 'mol':
            mol = mb_to_mol(value)
        else:
            raise TypeError
        smi, inchi, inchikey, mb = calc_output(mol)
        return Result(choice, value, smi, inchi, inchikey, mb)
    except Exception as e:
        print(e)
        return None
    
def smi_to_mol(value):
    return Chem.MolFromSmiles(value)

def inchi_to_mol(value):
    return Chem.MolFromInchi(value)

def inchikey_to_mol(value):
    smi = cactus_inchikey_lookup(value)
    return smi_to_mol(smi)

def mb_to_mol(value): 
    return Chem.MolFromMolBlock(value)
    
def calc_output(mol):
    smi = mol_to_smi(mol)
    inchi = mol_to_inchi(mol)
    inchikey = mol_to_inchikey(mol)
    mb = mol_to_mb(mol)
    return (smi, inchi, inchikey, mb)

def mol_to_smi(mol):
    return Chem.MolToSmiles(mol)

def mol_to_inchi(mol):
    return Chem.MolToInchi(mol)

def mol_to_inchikey(mol):
    return Chem.MolToInchiKey(mol)

def mol_to_mb(mol):
    return Chem.MolToMolBlock(mol)

def cactus_inchikey_lookup(inchikey):
    url = "https://cactus.nci.nih.gov/chemical/structure/{0}/smiles".format(inchikey)
    r = requests.get(url)
    if r.ok:
        smiles = r.text.split()
        if smiles:
            return smiles[0]
    raise NotImplementedError