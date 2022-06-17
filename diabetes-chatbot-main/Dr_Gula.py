from branch1 import *
import streamlit as st
from streamlit_chat import message
import pickle
import numpy as np

loaded_model = pickle.load(open('trained_model.sav', 'rb'))

st.set_page_config(
    page_title="Dr.Gula - Demo",
    page_icon=":robot:"
)
st.title("Dr.Gula")

if "details_state" not in st.session_state:
	st.session_state["details_state"] = False
	st.session_state["details"] = []

if 'count' not in st.session_state or st.session_state.count == 100: #limit chat per session
	st.session_state.count = 0 
	st.session_state.chat_history_ids = None
	st.session_state.old_response = ''
	st.session_state.history=[]
else:
 	st.session_state.count += 1

def start_chatbot():
	input=get_text()
	if input != "":
		get_ans(input)
	for chat in st.session_state.history[-6:]:
		message(**chat)
	if len(st.session_state.history) == 20:
		st.session_state.history=[]

def get_text():
	input = st.text_input("Message:",placeholder="Type here", key='input')
	return input

def get_ans(input):
	r1=False
	ans=input
	input=input.lower()
	if "bmi" in input:
		r1=True
		bmi=get_BMI()
		response=f"Your BMI is {round(bmi,2)}"
		if bmi < 16:
			response1="You are SEVERELY UNDERWEIGHT"
		elif bmi >= 16 and bmi <= 18.5:
			response1="You are UNDERWEIGHT"
		elif bmi >= 18.6 and bmi <= 25:
			response1="You are NORMAL WEIGHT"
		elif bmi >= 25.1 and bmi <= 30:
			response1="You are OVERWEIGHT"
		elif bmi >= 30.1 and bmi <= 35:
			response1="You are MODERATELY OBESE"
		else:
			response1="You are SEVERELY OBESE"

	elif input == "glucose" or input == "what is my glucose level":
		r1=True
		glucose = st.session_state.details[5]
		response = f"Your glucose level is {glucose}"
		if glucose <= 115:
			response1="Your glucose level is EXCELLENT"
		elif glucose > 115 and glucose <= 180:
			response1="Your glucose level is GOOD"
		else:
			response1="Your glucose level is POOR"

	elif input == "prediction" or input == "do i have diabetes":
		r1=True
		if pred[0] == 0:
			response="You do not have diabetes"
		else:
			response="You have diabetes"
		response1="However, my prediction may not be true. Please get diagnosed at the nearest hospital for more accurate result."

	else:
		response=chatbot_response(input)
	#add here

	st.session_state.history.append({"message": ans, "is_user": True, "key":2+st.session_state.count})
	st.session_state.history.append({"message": response,"key":1-st.session_state.count})
	if r1:
		st.session_state.history.append({"message": response1,"key":110+st.session_state.count})


def get_BMI():
	w = float(st.session_state.details[2])
	h = float(st.session_state.details[3])
	bmi=calc_BMI(w,h)
	return bmi

@st.cache()
def calc_BMI(w,h):
	return w/(h*h)

def pred_diabetes(input_data):
	prediction = loaded_model.predict(input_data)
	return prediction


if not st.session_state["details_state"]:
	st.header("Before using Dr. Gula Bot, please fill in these details first.")

	with st.form("details_form"):
		name = st.text_input("Name", placeholder="Enter your name", key="user_name")
		age = st.number_input("Age", min_value=1, max_value=100, value=18, step=1, key="user_age")
		weight = st.number_input("Weight (kg)", min_value=1.00, max_value=200.00, value=50.00, step=0.01, key="user_weight")
		height = st.number_input("Height (m)", min_value=0.10, max_value=3.00, value=1.50, step=0.01, key="user_height")
		pregnant = st.number_input("Number of times pregnant", min_value=0, max_value=30, value=0, step=1, key="user_pregnant")
		glucose = st.number_input("Glucose concentration (mg/dl)", min_value=0, max_value=300, value=0, step=1, key="user_glucose")
		bp = st.number_input("Blood pressure (mm Hg)", min_value=0, max_value=200, value=0, step=1, key="user_bp")
		skin = st.number_input("Skin thickness (mm)", min_value=0, max_value=200, value=0, step=1, key="user_skin")
		insulin = st.number_input("Insulin (mu U/ml)", min_value=0, max_value=2000, value=0, step=1, key="user_insulin")
		dpf = st.number_input("Diabetes Pedigree Function", min_value=0.00, max_value=10.00, value=0.00, step=0.01, key="user_dpf")

		submitted = st.form_submit_button("Submit")
		if submitted:
			st.session_state.details.append(name)
			st.session_state.details.append(age)
			st.session_state.details.append(weight)
			st.session_state.details.append(height)
			st.session_state.details.append(pregnant)
			st.session_state.details.append(glucose)
			st.session_state.details.append(bp)
			st.session_state.details.append(skin)
			st.session_state.details.append(insulin)
			st.session_state.details.append(dpf)
			st.session_state["details_state"] = True
			st.experimental_rerun()

else:
	name = st.session_state.details[0]
	age = st.session_state.details[1]
	weight = st.session_state.details[2]
	height = st.session_state.details[3]
	pregnant = st.session_state.details[4]
	glucose = st.session_state.details[5]
	bp = st.session_state.details[6]
	skin = st.session_state.details[7]
	insulin = st.session_state.details[8]
	dpf = st.session_state.details[9]
	bmi = calc_BMI(weight,height)

	input_data = (pregnant, glucose, bp, skin, insulin, bmi, dpf, age)
	input_data = np.asarray(input_data)
	input_data = input_data.reshape(1,-1)

	pred = pred_diabetes(input_data)

	start_chatbot()
