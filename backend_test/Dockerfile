FROM app-stack_backend

WORKDIR /code

RUN /usr/local/bin/pip install --user --no-cache-dir pytest-cov

CMD ["python", "-m", "pytest", "--cov", "rest_example"]
