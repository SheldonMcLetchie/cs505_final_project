FROM python:latest
RUN pip install flask
ADD main.py /cs505/main.py
WORKDIR /cs505
EXPOSE 9000
CMD ["main.py"]
ENTRYPOINT ["python"]