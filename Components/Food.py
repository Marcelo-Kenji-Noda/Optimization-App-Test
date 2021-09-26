import json
import os.path

import streamlit as st
import pandas as pd

class ListFoodItem:
    def __init__(self, foodlist):
        self.foodlist = foodlist
        return

    #Inicialize the foodlist with the json file
    def initialize_me(self):
        food_list = ListFoodItem([])
        file_exists = os.path.exists('foods.json')
        if file_exists:
            with open('foods.json', 'r') as f:
                data = json.load(f)
                food_list = ListFoodItem(
                    foodlist = self._get_foods_from_json(data)
                )
                return food_list
        else:
            return food_list
    
    def _get_foods_from_json(self, data):
        return_list = []
        for food in data['foodlist']:
            return_list.append(
                FoodItem(
                    name = food['name'],
                    protein=food['protein'],
                    calcium=food['calcium'],
                    cost = food['cost']
                )
            )
        self.foodlist = return_list
        return return_list

    def _foods_to_json(self):
        foodlist_ = []
        for food in self.foodlist:
            foodlist_.append(food.serialize())
        return foodlist_

    def serialize(self):
        return {
            'foodlist' : self._foods_to_json()
        }
    
    def food_list_to_pandas(self):
        df = pd.DataFrame([food.__dict__ for food in self.foodlist])
        return df



class FoodItem:
    def __init__(self, name, protein, calcium, cost):
        self.name = name
        self.protein = protein
        self.calcium = calcium
        self.cost = cost
        return

    def __str__(self):
        self.name

    def print_item(self):
        st.write(f"{self.name}: R${self.cost}")
        return

    def serialize(self):
        return {
            'name' : self.name,
            'protein' : self.protein,
            'calcium':self.calcium,
            'cost':self.cost,
        }

class Constraint:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def serialize(self):
        return {
            'name':self.name,
            'value':self.value
        }

class ConstraintList:
    def __init__(self, constraints):
        self.constraintslist = constraints

    #Inicialize the foodlist with the json file
    def initialize_me(self):
        constraint_list = ConstraintList([])
        file_exists = os.path.exists('constraints.json')
        if file_exists:
            with open('constraints.json', 'r') as f:
                data = json.load(f)
                constraint_list = ConstraintList(
                    constraints = self._get_constraints_from_json(data)
                )
                return constraint_list
        else:
            return constraint_list
    
    #Used to inicialize the json file
    def _get_constraints_from_json(self, data):
        return_list = []
        for constraint in data['constraint']:
            return_list.append(
                Constraint(
                    name = constraint['name'],
                    value = constraint['value']
                )
            )
        self.constraintslist = return_list
        return return_list

        
    #Used to serialize
    def _constraints_to_json(self):
        foodlist_ = []
        for constraint in self.constraintslist:
            foodlist_.append(constraint.serialize())
        return foodlist_

    def serialize(self):
        return {
            'constraint' : self._constraints_to_json()
        }

    def update_constraint_list(self, constraint):
        #Receives a constraint object type
        if constraint.name in [i.name for i in self.constraintslist]:
            aux = [i for i in self.constraintslist if i.name != constraint.name]
            self.constraintslist = aux
            self.constraintslist.append(constraint)
        else:
            self.constraintslist.append(constraint)

    def serialized_data(self):
        aux_list = []
        for i in range(len(self.constraintslist)):
            data = {'name':self.constraintslist[i].name,'value':self.constraintslist[i].value}
            aux_list.append(data)
        return aux_list

    def data_to_pandas(self):
        df = pd.DataFrame([constraint.__dict__ for constraint in self.constraintslist])
        return df