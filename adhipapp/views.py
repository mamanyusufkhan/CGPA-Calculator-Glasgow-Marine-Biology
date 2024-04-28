from django.shortcuts import render, redirect
from django.http import HttpResponse
from urllib.parse import parse_qs

grades = {
    'A1': 22,
    'A2': 21,
    'A3': 20,
    'A4': 19,
    'A5': 18,
    'B1': 17,
    'B2': 16,
    'B3': 15,
    'C1': 14,
    'C2': 13,
    'C3': 12,
    'D1': 11,
    'D2': 10,
    'D3': 9
}

threshold = {
    '1': [17.5, 25.1],
    '2:1': [14.5, 17.5],
    '2:2': [11.5, 14.5],
    '3': [8.5, 11.5]
}



optional_course = {
    'Applying Ecology': ['Presentation', 'Reflective Statement', 'Exam'],
    'Ecological Speciation': ['Poster', 'Poster Communication', 'Poster Reflection', 'Exam'],
    'Disease Ecology': ['Reflective Piece', 'Exam'],
    'Behavioural Ecology': ['Class Test', 'Exam'],
    'Tropical Marine Biology': ['Report', 'Reflective Statement', 'Exam'],
    'Fisheries, Aquaculture and Marine Conservation': ['Course Work', 'Exam']

}

weights = {
    'Applying Ecology Presentation': 0.025,
    'Applying Ecology Reflective Statement': 0.0125,
    'Applying Ecology Exam': 0.0875,
    'Ecological Speciation Poster': 0.025,
    'Ecological Speciation Poster Communication': 0.00625,
    'Ecological Speciation Poster Reflection': 0.00625,
    'Ecological Speciation Exam': 0.0875,
    'Disease Ecology Reflective Piece': 0.0375,
    'Disease Ecology Exam': 0.0875,
    'Behavioural Ecology Class Test': 0.0375,
    'Behavioural Ecology Exam': 0.0875,
    'Tropical Marine Biology Report': 0.025,
    'Tropical Marine Biology Reflective Statement': 0.0125,
    'Tropical Marine Biology Exam': 0.0875,
    'Fisheries, Aquaculture and Marine Conservation Course Work': 0.0375,
    'Fisheries, Aquaculture and Marine Conservation Exam': 0.0875,
    '3rd Year 3A': 0.125,
    '3rd Year 3B': 0.125,
    'Honours Project Presentation': 0.05,
    'Honours Project Report': 0.175,
    'Honours Project Supervisor\'s Assessment': 0.025,
    'Core Skills Essay': 0.05,
    'Core Skills Exam': 0.075
}

mandatory_course = {
    '3rd Year': ['3A', '3B'],
    'Honours Project': ['Presentation', 'Report', 'Supervisor\'s Assessment'],
    'Core Skills': ['Essay', 'Exam']
    
}

# Create your views here.
def index(request):
    keys = list(optional_course.keys())
    print(keys)
    context = {'optional_course': keys}

    
    if request.method == 'POST':
        optional_course_1 = request.POST.get('input1')
        optional_course_2 = request.POST.get('input2')
        optional_course_3 = request.POST.get('input3')

        selected_courses = {}
        selected_courses[optional_course_1] = optional_course[optional_course_1]
        selected_courses[optional_course_2] = optional_course[optional_course_2]
        selected_courses[optional_course_3] = optional_course[optional_course_3]

        total_courses = {**mandatory_course, **selected_courses}
        print(total_courses)

        keys = list(grades.keys())
        
        threshold_keys = list(threshold.keys())
        return render(request, 'calculation.html', {'my_dict': total_courses, 'grades': keys, 'threshold': threshold_keys})



    return render(request , 'index.html', context)

def calculate(request):
    
    if request.method == "POST":
        known = 0
        unknown = 0
        request_body = request.body
        request_body_str = request_body.decode('utf-8')

    
        parsed_data = parse_qs(request_body_str)

    
        parsed_data = {key: value[0] if len(value) == 1 else value for key, value in parsed_data.items()}
        del parsed_data['csrfmiddlewaretoken']
        print(parsed_data)

        prompt = parsed_data["prompt"]
        print(prompt)
        if prompt == "target":
            prompt_number = parsed_data["prompt_value"]
            del parsed_data["prompt"]
            del parsed_data["prompt_value"]
            for key, value in parsed_data.items():
                if value == 'Unknown':
                    unknown += weights[key]
                else:
                    known += grades[value] * weights[key]
            
            required_grade = (threshold[prompt_number][0] - known) / unknown
            print(required_grade)
            file = 'target.html'
            context = {'result': required_grade}

        elif prompt == "match":
            prompt_number = parsed_data["prompt_value"]
            del parsed_data["prompt"]
            del parsed_data["prompt_value"]
            for key, value in parsed_data.items():
                known += grades[value] * weights[key]
            

            print(known)
            text = ""
            range_value = threshold[prompt_number]
            if (range_value[0] <= known < range_value[1]):
                text = "Results Matched"
            else:
                text = "Results Did Not Match"

            print("It is coming here")
            file = 'match.html' 
            context = {'result': known, 'matched': text}

    return render(request, file, context)
    

    