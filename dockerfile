FROM python:3.9-slim
COPY ./src /app
COPY Pipfile* /app/
WORKDIR /app
RUN pip install pipenv
RUN pipenv install --system --deploy
ENTRYPOINT ["python"]
CMD ["app.py"]
