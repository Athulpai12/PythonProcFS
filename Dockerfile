FROM python:3.6.15

WORKDIR /usr/src/app

COPY . .

RUN python3 -m unittest SimpleProcParser/tests/test*

RUN export PYTHONDONTWRITEBYTECODE=1

CMD ["/bin/bash"]