# pull official base image
# docer에서 파이썬이 설치 되어 있는 것을 가져온다
FROM python:3.8-slim-buster

# set work directory
#파이썬이 설치 되어있는 가상 컴퓨터를 만들고 가상 컴퓨터에 폴더를 만들어 작업할 곳을 지정
WORKDIR /usr/src/app

# set environment variable
# .pyc 파일이 생성 되지 않도록 함
ENV PYTHONDONTWRITEBYTECODE 1
# 파이썬이 출력때 bufffering 하지 않게 해줌
ENV PYTHONBUFFERED 1


# 작업하고 있는 파일들을 저기 위치에 복사
COPY . /usr/src/app/

# install dependencies
# 업데이트
RUN pip install --upgrade pip

# requirements.txt에 있는 모든 버전 들이 설치가 되게 해준다.
RUN pip install -r requirements.txt
