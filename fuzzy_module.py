import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

attendance = ctrl.Antecedent(np.arange(0, 101, 1), 'attendance')
study_hours = ctrl.Antecedent(np.arange(0, 11, 1), 'study_hours')
prev_score = ctrl.Antecedent(np.arange(0, 101, 1), 'prev_score')
performance = ctrl.Consequent(np.arange(0, 101, 1), 'performance')

attendance.automf(3)
study_hours.automf(3)
prev_score.automf(3)

performance['low'] = fuzz.trimf(performance.universe, [0, 0, 50])
performance['medium'] = fuzz.trimf(performance.universe, [40, 60, 80])
performance['high'] = fuzz.trimf(performance.universe, [70, 100, 100])

rule1 = ctrl.Rule(attendance['good'] & study_hours['good'] & prev_score['good'], performance['high'])
rule2 = ctrl.Rule(attendance['average'] & study_hours['average'], performance['medium'])
rule3 = ctrl.Rule(attendance['poor'] | study_hours['poor'] | prev_score['poor'], performance['low'])

perf_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
perf_sim = ctrl.ControlSystemSimulation(perf_ctrl)

def predict_performance(att, hours, prev):
    perf_sim.input['attendance'] = att
    perf_sim.input['study_hours'] = hours
    perf_sim.input['prev_score'] = prev
    perf_sim.compute()
    return round(perf_sim.output['performance'], 2)