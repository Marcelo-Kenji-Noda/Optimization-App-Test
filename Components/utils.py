import json
import streamlit as st

def update_json(item, filename):
    with open(filename, 'w+') as json_file:
        json.dump(item.serialize(), json_file,
                indent=4)
    return