from flask import request, render_template, session, redirect, url_for
from app import app
from scipy.optimize import linprog
from app.utils.form_utils import *
from app.utils.post_optimization_utils import restrictions_right_change_dict_to_list
from app.utils.shadow_price_process import calculate_shadow_price


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template(
        'form.html',
        num_variables=0,
        num_restrictions=0,
        labels=[],
        objective_type='max',
        objective_values=[],
        restrictions_values=[],
        restrictions_right_values=[],
        restrictions_operator_values=[]
    )


@app.route('/initiate_simplex', methods=['GET', 'POST'])
def initiate_simplex():
    labels = []
    operators = ['<=', '>=']

    if request.method == 'POST':
        num_variables = int(request.form['num_variables'])
        num_restrictions = int(request.form['num_restrictions'])

        old_num_variables = session.get('num_variables')
        old_num_restrictions = session.get('num_restrictions')

        session['num_variables'] = num_variables
        session['num_restrictions'] = num_restrictions

        if old_num_variables != num_variables or old_num_restrictions != num_restrictions:
            session.pop('form_data', None)

    else:
        num_variables = session.get('num_variables')
        num_restrictions = session.get('num_restrictions')

    if num_variables and num_restrictions:
        labels = [chr(65 + i) for i in range(num_variables)]

    form_data = session.get('form_data', {})
    objective_type = session.get('objective_type', form_data.get('objective_type', 'max'))

    return render_template(
        'form.html',
        num_variables=num_variables if num_variables else 0,
        num_restrictions=num_restrictions if num_restrictions else 0,
        labels=labels,
        operators=operators,
        objective_type=objective_type,
        objective_values=form_data.get('objective_values', []),
        restrictions_values=form_data.get('restrictions_values', []),
        restrictions_right_values=form_data.get('restrictions_right_values', []),
        restrictions_operator_values=form_data.get('restrictions_operator_values', [])
    )


@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        objective_type = request.form.get('objective_type', 'max')
        session['objective_type'] = objective_type

        restrictions_right_values = dict_to_list({
            key: float(value)
            for key, value in request.form.items()
            if key.startswith('value_right')
        })

        objective_values = dict_to_list({
            key: float(value)
            for key, value in request.form.items()
            if key.startswith('variable')
        })

        num_variables = len(objective_values)
        num_restrictions = len(restrictions_right_values)

        restrictions_values = restrictions_dict_to_list({
            key: float(value)
            for key, value in request.form.items()
            if key.startswith('restriction')
        }, num_restrictions)

        restrictions_operator_values = [
            request.form.get(f'operator_{i}', '<=')
            for i in range(num_restrictions)
        ]

        restrictions_operators = {
            f'operator_{i}': restrictions_operator_values[i]
            for i in range(num_restrictions)
        }

        session['form_data'] = {
            'objective_type': objective_type,
            'objective_values': objective_values,
            'restrictions_values': restrictions_values,
            'restrictions_right_values': restrictions_right_values,
            'restrictions_operator_values': restrictions_operator_values
        }

        if objective_type == 'max':
            variables_list = [-value for value in objective_values]
        else:
            variables_list = objective_values

        calculation_restrictions_list = [row[:] for row in restrictions_values]
        calculation_restrictions_right_list = restrictions_right_values[:]

        calculation_restrictions_list, calculation_restrictions_right_list = invert_restriction_signs(
            restrictions_operators,
            calculation_restrictions_list,
            calculation_restrictions_right_list
        )

        session["restrictions_right_list"] = calculation_restrictions_right_list
        session["restrictions_operators"] = restrictions_operators
        session["variables_list"] = variables_list
        session["restrictions_list"] = calculation_restrictions_list

    else:
        calculation_restrictions_right_list = session.get('restrictions_right_list', [])
        restrictions_operators = session.get('restrictions_operators', {})
        variables_list = session.get('variables_list', [])
        calculation_restrictions_list = session.get('restrictions_list', [])
        objective_type = session.get('objective_type', 'max')

        if not variables_list or not calculation_restrictions_list:
            return redirect(url_for('home'))

        num_variables = len(variables_list)
        num_restrictions = len(calculation_restrictions_right_list)

    labels = [chr(65 + i) for i in range(num_variables)]

    result = linprog(
        variables_list,
        calculation_restrictions_list,
        calculation_restrictions_right_list,
        method="simplex"
    )

    shadow_price = calculate_shadow_price(
        result,
        variables_list,
        calculation_restrictions_list,
        calculation_restrictions_right_list
    )

    if objective_type == 'max':
        objective_fuction = -result.fun
    else:
        objective_fuction = result.fun

    return render_template(
        'result.html',
        objective_fuction=objective_fuction,
        variables_results=result.x,
        shadow_price=shadow_price,
        labels=labels,
        num_variables=num_variables,
        num_restrictions=num_restrictions,
        objective_type=objective_type
    )


@app.route('/sensitivity_analysis', methods=['GET', 'POST'])
def sensitivity_analysis():
    restriction_right_change_list = restrictions_right_change_dict_to_list({
        key: float(value)
        for key, value in request.form.items()
        if key.startswith('restriction_right_change')
    })

    variables_list = session.get('variables_list')
    restrictions_list = session.get('restrictions_list')
    restrictions_right_list = session.get('restrictions_right_list')
    objective_type = session.get('objective_type', 'max')

    if not variables_list or not restrictions_list or not restrictions_right_list:
        return redirect(url_for('home'))

    new_restrictions_right_list = [
        a + b
        for a, b in zip(restrictions_right_list, restriction_right_change_list)
    ]

    num_variables = len(variables_list)
    labels = [chr(65 + i) for i in range(num_variables)]

    new_result = linprog(
        variables_list,
        restrictions_list,
        new_restrictions_right_list,
        method="simplex"
    )

    if objective_type == 'max':
        objective_fuction = -new_result.fun
    else:
        objective_fuction = new_result.fun

    return render_template(
        'post_optimization.html',
        objective_fuction=objective_fuction,
        variables_results=new_result.x,
        result=new_result.status,
        num_variables=num_variables,
        num_restrictions=len(restrictions_right_list),
        labels=labels,
        objective_type=objective_type
    )


@app.route('/reset', methods=['GET'])
def reset():
    session.clear()
    return redirect(url_for('home'))