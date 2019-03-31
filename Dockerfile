FROM python:3.4-alpine

ENV APPLICATION_NAME simple_service

ADD .healthcheck.sh      /${APPLICATION_NAME}/
ADD src/requirements.txt /${APPLICATION_NAME}/
ADD src/code/*           /${APPLICATION_NAME}/src/

RUN chmod +x /${APPLICATION_NAME}/.healthcheck.sh

WORKDIR /${APPLICATION_NAME}/

RUN sh .healthcheck.sh

CMD ["python", "src/service.py"]
