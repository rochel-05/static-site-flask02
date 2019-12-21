FROM python:3.7

RUN mkdir /staticsiteflask3
WORKDIR /staticsiteflask3

COPY model /staticsiteflask3/model
COPY static /staticsiteflask3/static
COPY templates /staticsiteflask3/templates
COPY Dockerfile /staticsiteflask3
COPY extract_frames_from_video.py /staticsiteflask3
COPY invetigate_RF.py /staticsiteflask3
COPY requirements.txt /staticsiteflask3
COPY run.py /staticsiteflask3
COPY table.py /staticsiteflask3
COPY usersDb.db /staticsiteflask3

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "/staticsiteflask3/run.py"]