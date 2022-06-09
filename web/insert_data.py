# populating database with class information
   
from .models import * 
from web import db
from sqlalchemy.orm import sessionmaker
import os

majors_keys = ['id', 'short_name', 'full_name']
majors_data = [
    [2002, 'CS', 'Computational Sciences'],
    [2003, 'NS', 'Natural Sciences'],
    [2004, 'B', 'Business'],
    [2005, 'SS', 'Social Sciences'],
    [2006, 'AH', 'Arts and Humanities']
]

concentrations_keys = ['id', 'name','major_id']
concentrations_data = [
    [3001, 'Computational Theory and Analysis', 2002],
    [3002, 'Applied Problem Solving', 2002],
    [3003, 'Computer Science and Artificial Intelligence', 2002],
    [3004, 'Contemporary Knowledge Discovery', 2002],
    [3005, 'Data Science and Statistics', 2002],
    [3006, 'Mathematics', 2002],

    [3007, 'Humanities Analyses', 2006],
    [3008, 'Humanities Foundations', 2006],
    [3009, 'Humanities Applications', 2006],
    [3010, 'Historical Forces', 2006],
    [3011, 'Philosophy, Ethics, and the Law', 2006],
    [3012, 'Arts and Literature', 2006],

    [3013, 'Theoretical Foundations of Natural Science', 2003],
    [3014, 'Research Analyses in Natural Science', 2003],
    [3015, 'Problem Solving in Complex Systems', 2003],
    [3016, 'Molecules and Atoms', 2003],
    [3017, 'Cells and Organisms', 2003],
    [3018, "Earth's Systems", 2003],

    [3019, 'Theory and Analysis in the Social Sciences', 2005],
    [3020, 'Empirical Approaches to the Social Sciences', 2005],
    [3021, 'Designing Societies', 2005],
    [3022, 'Cognition, Brain, and Behavior', 2005],
    [3023, 'Economics and Society', 2005],
    [3024, 'Politics, Government, and Society', 2005],

    [3025, 'New Business Ventures', 2004],
    [3026, 'Scalable Growth', 2004],
    [3027, 'Enterprise Management', 2004],
    [3028, 'Brand Management', 2004],
    [3029, 'Strategic Finance', 2004],
    [3030, "Managing Operational Complexity", 2004]
    ]

# TODO add first year courses
courses_keys = ['id', 'short_name', 'long_name', 'type']
courses_data = [
    [4001, 'AH110', 'Global History', 'core'],
    [4002, 'AH111', 'Morality, Justice, and the Good Life', 'core'],
    [4003, 'AH112', 'The Arts and Social Change', 'core'],
    [4004, 'AH113', 'Dynamics of Design', 'core'],
    [4005, 'AH142', 'The Craft of Historical Analysis', 'concentration'],
    [4006, 'AH144', 'Ethical Systems, Moral Dilemmas', 'concentration'],
    [4007, 'AH146', 'Decoding Art and Literature', 'concentration'],
    [4008, 'AH152', 'Comparing Societies and Histories: The Impact of Time and Place', 'concentration'],
    [4009, 'AH154', 'Ethics and the Law', 'concentration'],
    [4010, 'AH156', 'Socioeconomic Influences on Art and Literature', 'concentration'],
    [4011, 'AH162', 'Public and Applied History', 'concentration'],
    [4012, 'AH164', 'Social and Political Philosophy', 'concentration'],
    [4013, 'AH166', 'Artistic Communication from Page to Practice', 'concentration'],

    [4014, 'CS110', 'Problem Solving with Data Structures and Algorithms', 'core'],
    [4015, 'CS111', 'Single and Multivariable Calculus', 'core'],
    [4016, 'CS113', 'Theory and Applications of Linear Algebra', 'core'],
    [4017, 'CS114', 'Probability and Statistics and the Structure of Randomness', 'core'],
    [4018, 'CS142', 'Theory of Computation', 'concentration'],
    [4019, 'CS144', 'Real Analysis', 'concentration'],
    [4020, 'CS146', 'Computational Methods for Bayesian Statistics', 'concentration'],
    [4021, 'CS152', 'Theory and Applications of Artificial Intelligence', 'concentration'],
    [4022, 'CS154', 'Analytical and Numerical Methods in Differential Equations', 'concentration'],
    [4023, 'CS156', 'Finding Patterns in Data with Machine Learning', 'concentration'],
    [4024, 'CS162', 'Software Engineering: Building Powerful Applications', 'concentration'],
    [4025, 'CS164', 'Optimization Methods', 'concentration'],
    [4026, 'CS166', 'Modeling and Analysis of Complex Systems', 'concentration'],

    [4027, 'B110', 'Market Dynamics and Product Analytics', 'core'],
    [4028, 'B111', 'Financial Planning, Budgeting and Modeling', 'core'],
    [4029, 'B112', 'Doing Business', 'core'],
    [4030, 'B113', 'Enterprise, Design and Optimization', 'core'],
    [4031, 'B144', 'Needs Identification and Product Development', 'concentration'],
    [4032, 'B145', 'Venture Initiation and Valuation', 'concentration'],
    [4033, 'B146', 'Business Operations', 'concentration'],
    [4034, 'B154', 'Strategic Brand Leadership', 'concentration'],
    [4035, 'B155', 'Capital Allocation and Value Creating Growth', 'concentration'],
    [4036, 'B156', 'Business Systems', 'concentration'],
    [4037, 'B164', 'Product Evolution and Reinvention', 'concentration'],
    [4038, 'B165', 'Global Enterprise Financial Strategy', 'concentration'],
    [4039, 'B166', 'Business Optimization', 'concentration'],

    [4040, 'NS110L', 'Physics of Life', 'core'],
    [4041, 'NS110U', 'Physics of the Universe', 'core'],
    [4042, 'NS111', "Implications of Earth's Cycles", 'core'],
    [4043, 'NS112', 'Evolution Across Multiple Scales', 'core'],
    [4044, 'NS142', 'Quantum Nature of Matter: Theory and Applications', 'concentration'],
    [4045, 'NS144', 'Genes to Organisms', 'concentration'],
    [4046, 'NS146', "Integrating Earth's Systems", 'concentration'],
    [4047, 'NS152', 'Analyzing Matter and Molecules', 'concentration'],
    [4048, 'NS154', "Life's Chemistry", 'concentration'],
    [4049, 'NS156', "Monitoring and Modeling Earth's Systems", 'concentration'],
    [4050, 'NS162', 'Statistical Mechanics: Theory and Applications', 'concentration'],
    [4051, 'NS164', 'Solutions From and For Life', 'concentration'],
    [4052, 'NS166', 'Keeping Earth Habitable', 'concentration'],
    [4053, 'NS113', 'Chemical Structure and Reactivity', 'core'],

    [4054, 'SS110', 'Psychology: From Neurons to Society', 'core'],
    [4055, 'SS111', 'Modern Economic Thought', 'core'],
    [4056, 'SS112', 'Political Science and Social Change', 'core'],
    [4057, 'SS142', 'Theories of Cognition and Emotion', 'concentration'],
    [4058, 'SS144', 'Intermediate Economic Theory and Tools', 'concentration'],
    [4059, 'SS146', 'Practice of Governance', 'concentration'],
    [4060, 'SS152', 'Cognitive Neuroscience', 'concentration'],
    [4061, 'SS154', 'Econometrics and Economic Systems', 'concentration'],
    [4062, 'SS156', 'Comparative Politics in Practice', 'concentration'],
    [4063, 'SS162', 'Personal and Social Motivation', 'concentration'],
    [4064, 'SS164', 'Global Development and Applied Economics', 'concentration'],
    [4065, 'SS166', 'Comparative Constitutional Law: Designing Societies', 'concentration']
]

# TODO add here 
course_concentration_keys = ['id','course_id', 'concentration_id']
course_concentration_data = [
    [8001, 4065, 3024],
    [8002, 4062, 3024],
    [8003, 4020, 3005]
]

professors_keys = ['id', 'first_name', 'last_name']
professors_data = [
    [5001, 'Phillip', 'Stern'],
    [5002, 'Nicki', 'Eberhard'],
    [5003, 'Nicholas', 'Kenney']
]


keys = [majors_keys, concentrations_keys, courses_keys, course_concentration_keys,professors_keys]
data_values = [ majors_data, concentrations_data, courses_data, course_concentration_data,professors_data]
tables = [Major, Concentration, Course, Course_concentration, Professor]

def add_new_entries(keys, data_values, tables):
    '''
        This function adds entries to the table using keys, values and table names.
    '''
    temp = []
    for value in data_values:
        dict_temp = dict(zip(keys, value))
        temp.append(dict_temp)
    
    for single_entry in temp:
        entry = tables(**single_entry)
        db.session.add(entry)

for i in range(len(tables)):
    add_new_entries(keys[i], data_values[i], tables[i])

db.session.commit()
db.session.close()
