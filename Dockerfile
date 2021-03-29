FROM python:3.8.3

ENV HOME=/opt/app DJANGO_SETTINGS_MODULE=app.settings

WORKDIR $HOME

COPY requirements.txt $HOME
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY . $HOME

EXPOSE 80

ENV PYTHONUNBUFFERED=true

CMD sh config/run.sh
