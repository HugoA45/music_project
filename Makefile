run:
	@uvicorn fast:app --reload

website:
	@streamlit run website_test.py
