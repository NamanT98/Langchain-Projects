FROM python:3.11.6
WORKDIR /app

COPY main.py /app/
COPY helper.py /app/
COPY requirements.txt /app/

RUN pip install -r requirements.txt
EXPOSE 8501
CMD [ "streamlit","run","./main.py" ]