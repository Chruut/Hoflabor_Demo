# Hoflabor_Demo
Interactive Dashboard/Web-App of simulated environmental field data taken from hypothetical farm

## Preview
![firefox_jOIDtQYPwv](https://github.com/user-attachments/assets/be91e9d3-cba6-4ce2-b590-a6674efdc746)

## Description
A simulation of temperature, soil humidity and biodiversity data is created in "daten_simulator.py" which creates a .csv file with the data.
The main application is "dashboard.py" where the .csv data is fed into a pipeline and prepared to be displayed as panels in a Web-Browser. 

## How to run the script
1. Download all the files into a folder
2. Open the folder in your IDE (i.e. Visual Studio Code)
3. Create a .venv programming environment
4. Install the package requirements using the requirements.txt file:
pip install -r requirements.txt  
5. Host the Website 
   In the terminal of the programming environment run: panel serve dashboard.py --dev
6. Visit the website that is printed in the terminal 
   
