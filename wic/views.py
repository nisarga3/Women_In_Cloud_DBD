from django.shortcuts import render,redirect
from django.http import HttpResponse
import asyncio
import json
import requests
import pyrebase
from django.contrib import auth
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.

# Sign in and login

config={
    "apiKey": "AIzaSyDhJzTtzvQPqUcNIh9RcZYfGBsDksGh42Y",
    "authDomain": "restfulcoe.firebaseapp.com",
    "projectId": "restfulcoe",
    "storageBucket": "restfulcoe.appspot.com",
    "messagingSenderId": "146950354250",
    "appId": "1:146950354250:web:e325943282e9686c2efdb3",
    "measurementId": "G-53E7HVRZVK",
    "databaseURL":""
}

firebase=pyrebase.initialize_app(config)
authh=firebase.auth()

def signin(request):
    if 'email' in request.session:
        email = request.session['email']
        if email == "wicadmin@rvce.edu.in":
            return render(request,"admin_index.html",{"e":email})
        else:
            # hiredstuff
            response = requests.get(f'https://springbootapi-production-c1e0.up.railway.app/usn/{email}')
            student_usn = response.json()
            print(student_usn['USN'])
            url='https://springbootapi-production-c1e0.up.railway.app/student'
            payload = json.dumps({
                    "USN": student_usn['USN'],
                })
            headers = {
                    'Content-Type': 'application/json'
                }
            student = requests.request("POST",  url, headers=headers, data=payload)
            print(student.json())
            return render(request,"stud_index.html",{"stud":student.json()})
    else:
        return render(request,'signin.html')

    
def postsignin(request):
    url = "https://springbootapi-production-c1e0.up.railway.app/register-student"
    email=request.POST.get('email')
    password=request.POST.get('pass')
    
    try:
        user=authh.sign_in_with_email_and_password(email,password)
    except:
        message="Invalid Credentials"
        return render(request,"signin.html",{"msg":message})
    # print(user['idToken'])
    # session_id=user['idToken']
    # request.session['uid']=str(session_id)
    request.session['email'] = email
    if(email=="wicadmin@rvce.edu.in" and password=="admin123"):
        return render(request,"admin_index.html",{"e":email})
    else:
        # getusn_stud(email)
        html1=render(request,"stud_index.html",{"e":email})
        #send data
        stud=getusn_stud(email)
        # print(response)
        request.session['email'] = email
        response = requests.get(f'https://springbootapi-production-c1e0.up.railway.app/usn/{email}')
        student_usn = response.json()
        print(student_usn['USN'])
        url='https://springbootapi-production-c1e0.up.railway.app/student'
        payload = json.dumps({
                    "USN": student_usn['USN'],
                })
        headers = {
                'Content-Type': 'application/json'
            }
        student = requests.request("POST",  url, headers=headers, data=payload)
        print(student.json())
        html1= render(request,"stud_index.html",{"stud":student.json()})
        html2=render(request,"studetails.html",{"stud":stud})
         # save html2 to the session
        request.session['html2'] = html2.content.decode('utf-8')
        print(type(html2))
        return html1

def logout(request):
    auth.logout(request)
    # del request.session['email']
    return render(request,"signin.html")

def signup(request):
    if 'email' in request.session:
        return render(request,"stud_index.html",{"e":request.session['email']})
    else:
        return render(request,"signup.html")


def postsignup(request):
    url = "https://springbootapi-production-c1e0.up.railway.app/register-student"
    email=request.POST.get('email')
    password=request.POST.get('pass')
    first_name=request.POST.get('Firstname')
    last_name=request.POST.get('Lastname')
    batch=request.POST.get('batch')
    usn=request.POST.get('usn')
    dep=request.POST.get('dept')
    phone_num=request.POST.get('phno')
    resume=request.POST.get('resume')
    try:
        user=authh.create_user_with_email_and_password(email,password)
        payload = json.dumps({
            "usn": usn,
            "batch": batch,
            "department": dep,
            "email_id": email,
            "student_first_name": first_name,
            "student_mid_name": resume,
            "student_last_name": last_name,
            "phone_number": phone_num
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
    except:
        message="Unable to create account, Try Again!"
        return render(request,"signup.html",{"msg":message})
    # uid=user['localId']
    # data = {"name": f"{first_name} {last_name}", "status": "1"}
    # database.child("users").child(uid).child("details").set(data)
    # request.session['uid']=str(session_id)
    
    return render(request,"signin.html",{"msg":f'Account created for {email}!'})
# ----DEFAULT PAGE----
def index(request):
    return render(request, 'index.html')

def adview(request):
    return render(request,'admin_index.html')

def stview(request):
    return render(request,'stud_index.html')

def getusn_stud(email):
    response = requests.get(f'https://springbootapi-production-c1e0.up.railway.app/usn/{email}')
    student_usn = response.json()
    print(student_usn['USN'])
    url='https://springbootapi-production-c1e0.up.railway.app/student'
    payload = json.dumps({
            "USN": student_usn['USN'],
        })
    headers = {
            'Content-Type': 'application/json'
        }
    student = requests.request("POST",  url, headers=headers, data=payload)
    stud_details=student.json()
    print(stud_details)
    return stud_details

    # return render('studetails.html',{"studs":stud_details})

def getstud(request):
    # retrieve the saved html2 variable from the session
    html2_str = request.session.get('html2', '')
    # render the HTML content as a template
    html2_template = render(request, 'try.html', {'content': html2_str})
    # return the rendered HTML template to the client
    return html2_template

def dashboard(request):
    return render(request,'powerbi.html')

def powerbi(request):
    return render(request,'powerbi.html')

# --PROJECTS--
def addproj(request):
    return render(request,"projects/add-project.html")

# Add new project
def addproject(request):
    url="https://springbootapi-production-c1e0.up.railway.app/add-project"
    compname=request.POST.get('Companyname')
    desc=request.POST.get('description')
    req=request.POST.get('requirements')
    mngr=request.POST.get('manager')
    stdate=request.POST.get('startdate')
    enddate=request.POST.get('enddate')
    opening=request.POST.get('openingproj')
    projres=request.POST.get('projresources')
    staff=request.POST.get('staffproj')
    try:
        payload = json.dumps({
            "company_name": compname,
            "description": desc,
            "requirements": req,
            "manager": mngr,
            "start_date": stdate,
            "end_date": enddate,
            "opening": opening,
            "resources": projres,
            "staff_incharge": staff,
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response)
        
    except:
        message="Unable to add project, Try Again!"
        return render(request,"admin_index.html",{"msg":message})    
    return render(request,"admin_index.html")

def projectview(request):
    response = requests.get('https://springbootapi-production-c1e0.up.railway.app/projects')
    projects = response.json()
    # if response is None or len(response) == 0:
    #     return JsonResponse({'messageproj': 'No projects found'})
    # else:
    return render(request,"projects/projects.html",{"projs":projects})

def stud_view_proj(request):
    response = requests.get('https://springbootapi-production-c1e0.up.railway.app/projects')
    projects = response.json()
    # if response is None or len(response) == 0:
    #     return JsonResponse({'messageproj': 'No projects found'})
    # else:
    return render(request,"projects/stud-proj.html",{"projs":projects})

def apply_proj(request,project_id,USN):
    url='https://springbootapi-production-c1e0.up.railway.app/apply-project'
    payload = json.dumps({
            "USN": USN,
            "project_id":project_id,
        })
    headers = {
            'Content-Type': 'application/json'
        }
    response = requests.request("POST",  url, headers=headers, data=payload)
    print(response)
    if(str(response)=="<Response [500]>"):
        return JsonResponse({"message":"Sorry, You have a ongoing Project and we do not allow multiple applications. Feel free to email us."})
    return redirect('/apply_projects')


def applied_students_proj(request,project_id):
    response = requests.get(f'https://springbootapi-production-c1e0.up.railway.app/project-applied-students/{project_id}/')
    studs = response.json()
    return render(request,"projects/applied_proj.html",{"studs":studs,"pid":project_id})

def hire_proj(request,USN,project_id):
    url='https://springbootapi-production-c1e0.up.railway.app/hire-project'
    payload = json.dumps({
            "USN": USN,
            "project_id":project_id,
        })
    headers = {
            'Content-Type': 'application/json'
        }
    response = requests.request("POST",  url, headers=headers, data=payload)
    return redirect(f'/applied_students_projects/{project_id}')


# --INTERNSHIPS--
def internshipview(request):
    response = requests.get('https://springbootapi-production-c1e0.up.railway.app/internships')
    internships = response.json()
    # if response is None or len(response) == 0:
    #     return JsonResponse({'messageintern': 'No internships found'})
    # else:
    return render(request,"internships/internships.html",{"interns":internships})

def stud_view_intern(request):
    response = requests.get('https://springbootapi-production-c1e0.up.railway.app/internships')
    internships = response.json()
    # if response is None or len(response) == 0:
    #     return JsonResponse({'messageintern': 'No internships found'})
    # else:
    return render(request,"internships/stud-intern.html",{"interns":internships})

def addintern(request):
    return render(request,"internships/add-internship.html")

# Add new internship

def addinternship(request):
    url="https://springbootapi-production-c1e0.up.railway.app/add-internship"
    compname=request.POST.get('Companyname')
    desc=request.POST.get('roledescription')
    req=request.POST.get('requirements')
    mngr=request.POST.get('manager')
    stdate=request.POST.get('startdate')
    enddate=request.POST.get('enddate')
    opening=request.POST.get('opening')
    location=request.POST.get('location')
    mode=request.POST.get('mode')
    typee=request.POST.get('type')
    
    try:
        payload = json.dumps({
            "company_name": compname,
            "role_description": desc,
            "requirements": req,
            "manager": mngr,
            "start_date": stdate,
            "end_date": enddate,
            "mode":  mode,
            "location": location,
            "type": typee,
            "opening":opening,
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response)
    except:
        message="Unable to add internship, Try Again!"
        return render(request,"admin_index.html",{"msg":message})    
    return render(request,"admin_index.html")

def apply_intern(request,internship_id,USN):
    url='https://springbootapi-production-c1e0.up.railway.app/apply-internship'
    payload = json.dumps({
            "USN": USN,
            "internship_id":internship_id,
        })
    headers = {
            'Content-Type': 'application/json'
        }
    response = requests.request("POST",  url, headers=headers, data=payload)
    print(response)
    if(str(response)=="<Response [500]>"):
        return JsonResponse({"message":"Sorry, You have a ongoing Internship and we do not allow multiple applications. Feel free to email us."})
    return redirect('/apply_internships')


def applied_students_intern(request,internship_id):
    response = requests.get(f'https://springbootapi-production-c1e0.up.railway.app/internship-applied-students/{internship_id}/')
    studs = response.json()
    return render(request,"internships/applied_intern.html",{"studs":studs,"iid":internship_id})

def hire_intern(request,USN,internship_id):
    url='https://springbootapi-production-c1e0.up.railway.app/hire-internship'
    payload = json.dumps({
            "USN": USN,
            "internship_id":internship_id,
        })
    headers = {
            'Content-Type': 'application/json'
        }
    response = requests.request("POST",  url, headers=headers, data=payload)
    return redirect(f'/applied_students_internships/{internship_id}')

# --EVENTS--
def addeve(request):
    return render(request,"events/add-event.html")

# Add new event
def addevent(request):
    url="https://springbootapi-production-c1e0.up.railway.app/add-event"
    eventname=request.POST.get('eventname')
    desc=request.POST.get('description')
    stdate=request.POST.get('startdate')
    enddate=request.POST.get('enddate')
    location=request.POST.get('location')
    staff_incharge=request.POST.get('staff')
    typee=request.POST.get('type')
    poster=request.POST.get('poster')

    try:
        payload = json.dumps({
            "description": desc,
            "end_date": enddate,
            "location": location,
            "name": eventname,
            "poster":poster,
            "staff_incharge":staff_incharge,
            "start_date": stdate,
            "type": typee,

        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response)
        
    except:
        message="Unable to add event, Try Again!"
        return render(request,"admin_index.html",{"msg":message})    
    return render(request,"admin_index.html")

def eventview(request):
    response = requests.get('https://springbootapi-production-c1e0.up.railway.app/events')
    events = response.json()
    # if response is None or len(response) == 0:
    #     return JsonResponse({'messageevent': 'No events found'})
    # else:
    return render(request,"events/events.html",{"events":events})

def stud_view_event(request):
    response = requests.get('https://springbootapi-production-c1e0.up.railway.app/events')
    events = response.json()
    # if response is None or len(response) == 0:
    #     return JsonResponse({'messageevent': 'No events found'})
    # else:
    return render(request,"events/stud-event.html",{"events":events})

def apply_event(request,event_id,USN):
    url='https://springbootapi-production-c1e0.up.railway.app/apply-event'
    payload = json.dumps({
            "USN": USN,
            "event_id":event_id,
        })
    headers = {
            'Content-Type': 'application/json'
        }
    response = requests.request("POST",  url, headers=headers, data=payload)
    print(response)
    if(str(response)=="<Response [500]>"):
        return JsonResponse({"message":"Sorry, You have a ongoing Project and we do not allow multiple applications. Feel free to email us."})
    return redirect('/apply_events')


def applied_students_event(request,event_id):
    response = requests.get(f'https://springbootapi-production-c1e0.up.railway.app/event-applied-students/{event_id}/')
    studs = response.json()
    return render(request,"events/applied_event.html",{"studs":studs,"eid":event_id})

def archivedeve(request):
    response = requests.get('https://springbootapi-production-c1e0.up.railway.app/events-archived')
    events = response.json()
    print(events)
    return render(request,"events/stud-event.html",{"events":events})


# # --DOWNLOAD REPORTS
# def export_csv(request):
#     response= HttpResponse(content_type='text/csv')

#     response['Content-Disposition'] = 'attachment; filename=Internships' + str(datetime.datetime.now())+ '.csv'
#     writer = csv.writer(response)
#     writer.writerow(['COMPANY NAME', 'REQUIREMENTS', 'START DATE/END DATE', 'NUMBER OF OPENINGS'])

def get_company_logo(company_name):
    print(company_name)
    url = f"https://logo.clearbit.com/{company_name}.com"
    response = requests.get(url)
    if response.status_code == 200:
        # If the API returns a successful response, return the logo URL
        return url
    else:
        # If the API returns an error response, return None
        return None