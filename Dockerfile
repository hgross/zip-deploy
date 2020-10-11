FROM python:3.8
WORKDIR /code

# for once, we have "no" dependencies. Yay! ;-)
#COPY requirements.txt .
#RUN pip install -r requirements.txt

COPY zipdeploy/ ./zipdeploy/

CMD [ "python", "-m", "zipdeploy.zipdeploy"] 