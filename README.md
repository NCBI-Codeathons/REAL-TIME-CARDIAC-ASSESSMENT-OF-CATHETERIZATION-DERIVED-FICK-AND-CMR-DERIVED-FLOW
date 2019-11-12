# REAL-TIME CARDIAC ASSESSMENT OF CATHETERIZATION-DERIVED FICK AND CMR-DERIVED FLOW
## INSTALLATION

 - install python 3
 - add python to your path
 - If Python is installed correctly and added to path, the following command should print the Python version number
 ```sh
$ Python --version
```
 - In the terminal, go into the project's directory and run the following command to install the requirements
  ```sh
$ pip install -r requirements.txt
```
 - add FLASK_APP to path
 ```sh
$ export FLASK_APP=app.py
```
- Run the flask app
```sh
$ flask run
```
- It shows the address at which the app is deployed. Go to this address on a web browser
- For production deployment, deploy the app using Nginx + Gunicorn

 

## BACK GROUND 
Cardiologists are tasked with the role of determining complex hemodynamic information that is important to determine the need for catheter-based and/or surgical intervention. Today’s standard of care practice involves performing cardiac catheterization and cardiac magnetic resonance (CMR) separately. Catheterization by x-ray is used primarily to collect pressure and saturation data and to intervene on hemodynamically significant holes in the heart. In addition, interventionalists are able to place stents, coils, and percutaneous valves. Meanwhile, CMR is a powerful emerging tool to help cardiologists and CT surgeons answer complex physiology questions by showing very accurate function and flow data.  

Interventional cardiac magnetic resonance (iCMR) is a new approach in congenital cardiology gaining traction around the world. In the US, the National Institutes of Health (NIH) and Children’s Health Dallas are the only two centers currently actively pursuing this research in the congenital heart population. iCMR is like a normal heart catheterization, but the procedure occurs in the MRI magnet instead of the catheterization X-ray lab. It is our hope that a radiation-free heart catheterization will become standard of care for patients in the future. 

We would like to improve the workflow and ease of calculating important hemodynamic information derived by cardiac catheterization, CMR, and/or iCMR. These numbers are important because they will help guide therapy and are often what surgeons and cardiologists analyze to determine if intervention is necessary. Cardiac catheterization and CMR use different techniques to ultimately produce the same hemodynamic information.  Both techniques use simple but unrelated equations to determine the patient’s systemic and pulmonary cardiac flows. The current workflow of using these equations is completely manual and subject to human error. 

Our goal is to improve workflow, reliability, and reproducibility by improving the accessibility of these hemodynamic equations through a web/app-based user-friendly display that will allow the operator to obtain information in real time.

Team Lead: Yousef Arar, MD, MPH, Pediatric Cardiology, www.utsouthwestern.edu/education/medical-school/departments/pediatrics/divisions/cardiology/

![alt text](https://images.squarespace-cdn.com/content/v1/5b3ffc3fcef3721bd81d8c60/1559313457968-QPMI423J93ITGQAD7VTW/ke17ZwdGBToddI8pDm48kCGpf5kg6I8N1YOl6KoZZklZw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZamWLI2zvYWH8K3-s_4yszcp2ryTI0HqTOaaUohrI8PIekhbcyIhvVCXt9CC6snuWfXbYWE8-PqfAVzApY0fWXIKMshLAGzx4R3EDFOm1kBS/arar1.jpg?format=2500w)
