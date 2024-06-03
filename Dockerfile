FROM python:3.9

WORKDIR /home

COPY pyproject.toml .
COPY main.py .
COPY README.md .

RUN pip install poetry
RUN poetry install

CMD ["python", "main.py"]



