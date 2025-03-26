python -m virtualenv -p python3.8 venv
venv\Scripts\activate
python -m pip install -r requirements.windows.txt
streamlit run app.py