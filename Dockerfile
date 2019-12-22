FROM python:3.7

RUN mkdir /staticsiteflask4
WORKDIR /staticsiteflask4

COPY model /staticsiteflask4/model
COPY static /staticsiteflask4/static
COPY templates /staticsiteflask4/templates
COPY Dockerfile /staticsiteflask4
COPY extract_frames_from_video.py /staticsiteflask4
COPY invetigate_RF.py /staticsiteflask4
COPY requirements.txt /staticsiteflask4
COPY run.py /staticsiteflask4
COPY table.py /staticsiteflask4
COPY usersDb.db /staticsiteflask4

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "/staticsiteflask4/run.py"]
