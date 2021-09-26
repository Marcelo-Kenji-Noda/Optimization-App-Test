from ortools.linear_solver import pywraplp
from Components.Food import FoodItem, ListFoodItem, ConstraintList, Constraint
from Components.utils import update_json
import pandas as pd

import streamlit as st
import json

#Global variable
food_list = ListFoodItem([])
food_list.initialize_me()

constraint_list = ConstraintList([])
constraint_list.initialize_me()

def MinimizeFunction(dataframe, constraints):
    solver = pywraplp.Solver.CreateSolver('SCIP')

    foods = [solver.NumVar(0.0, solver.infinity(), name=name) for name in dataframe['name']]

    nvariables = solver.NumVariables()

    objective = solver.Objective()

    for constraint in constraints.constraintslist:
        solver.Add(solver.Sum([foods[i]*dataframe[constraint.name][i] for i in range(len(foods))]) >= constraint.value)

    for i ,food in enumerate(foods):
        objective.SetCoefficient(food, dataframe['cost'][i])
    
    solver.Add(solver.Sum([food for food in foods]) == 1)
    objective.SetMinimization()
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        st.markdown('---------------------------------------')
        st.write('Solution:')
        st.write('Objective value =', solver.Objective().Value())
        for food in foods:
            if food.solution_value() > 0.01:
                st.write(food.name() , food.solution_value(),"kg")
    else:
        st.write('The problem does not have an optimal solution.')

    return {
        'nvariables':nvariables,
        'status':status
    }

# Instantiate a Glop solver and naming it.
def AddFoodForms(food_list):
    with st.expander("Add Food Forms 🥐"):
        #Initizalizing Forms
        form = st.form(key="add_form")

        #Food Inputs
        name = form.text_input("Name of the food")
        cost = form.number_input("Cost ($/kg)")
        protein = form.number_input("Protein")
        calcium = form.number_input("Calcium")

        #Submit button
        submit = form.form_submit_button('Submit')

        #onSubmit
        if submit:
            #Create and append the food to the foodlist
            newfood = FoodItem(name=name, cost=cost, protein= protein, calcium = calcium)
            food_list.foodlist.append(newfood)

            #Write item into the json file
            update_json(item = food_list,filename ='foods.json')

            return newfood
        else:
            return

def FoodFormsConstraints(constraint_list):
    with st.expander("Add the constraints ⛓️"):
        form_2 = st.form(key="constraint_forms")

        calcium_constraint =  form_2.number_input("Maximum Calcium", key="calcium_constraint")
        protein_constraint = form_2.number_input("Maximum Protein", key="protein_constraint")

        submit_button = form_2.form_submit_button('Submit')

        if submit_button:
            constraint01 = Constraint(name="calcium", value=calcium_constraint)
            constraint02 = Constraint(name="protein", value=protein_constraint)

            constraint_list.update_constraint_list(constraint01)
            constraint_list.update_constraint_list(constraint02)

            update_json(item = constraint_list, filename ='constraints.json')
    return

def FoodMixesPages():

    FoodFormsConstraints(constraint_list)
    AddFoodForms(food_list)

    df = food_list.food_list_to_pandas()
    constraint_df = constraint_list.data_to_pandas()

    if not df.empty:
        st.markdown("## Dataframe with the food")
        st.dataframe(df)
        cleardataframe = st.button(" 🗑️ Delete Dataframe")
        if cleardataframe:
            food_list.foodlist.clear()
            update_json(item=food_list, filename='foods.json')

        res = MinimizeFunction(dataframe=df, constraints=constraint_list)
        status = res['status']
        st.write(res["nvariables"])
    else:
        st.markdown("No item added to the dataframe 😓")


    if not constraint_df.empty:
        st.dataframe(constraint_df)
        clearconstraints = st.button(" 🗑️ Delete Constraint")
        if clearconstraints:
            constraint_list.constraintslist.clear()
            update_json(item=constraint_list, filename='constraints.json')
    else:
        st.markdown("No constraint added")
    return