#Pull base image
FROM python:3.6
RUN pip3 install --upgrade pip
#Copy code into image and making it as a working directory
COPY . /application
WORKDIR /application
RUN pip3 --no-cache-dir install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["hello.py"]


