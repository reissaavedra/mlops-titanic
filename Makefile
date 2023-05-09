all_tests:
	pytest -v  --cov --cov-report=xml

flake:
	flake8 /home/reisson/TUL/mlops-titanic/.flake8 --show-source --statistics