from aqt import mw
import pathlib
import importlib.util
import sys
import re
import os

def importLocalDependency(name: str):
    addon_root = pathlib.Path(__file__).resolve().parent
    dep_source = addon_root / "lib" / name / "__init__.py" 
    spec = importlib.util.spec_from_file_location(name, dep_source)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)

def getCommonFields(selected_notes):
    
    common_fields = set()

    first = True

    for note_id in selected_notes:
        note = mw.col.get_note(note_id)
        if note is None: 
            raise Exception(f"Note with id {note_id} is None.\nNotes: {','.join([mw.col.get_note(id) for id in selected_notes])}.")
        model = note.note_type()
        model_fields = set([f['name'] for f in model['flds']])
        if first:
            common_fields = model_fields # Take the first one as is and we will intersect it with the following ones
        else:
            common_fields = common_fields.intersection(model_fields) # Find the common fields by intersecting the set of all fields together
        first = False
    return common_fields

def cleanFieldText(text: str)->str:
    tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
    entity_re = re.compile(r'(&[^;]+;)')

    text = entity_re.sub('', text)
    text = tag_re.sub('', text)

    text = re.sub("\[.*?\]", "", text)
    text = re.sub(" ", "", text)

    return text

def removeFile(file:str):
   os.remove(file) 