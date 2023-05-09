all_tests:
	pytest --html=outputs/pytest-report.html

flake:
	flake8 /home/reisson/TUL/mlops-titanic/.flake8 --show-source --statistics