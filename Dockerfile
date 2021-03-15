FROM python3.8 AS receitas

ENV PORT 5000

WORKDIR "$HOME/app"

COPY . .

# Install pip requirements
COPY requirements.txt ./
RUN pip install -r requirements.txt

ENTRYPOINT ["./entrypoint"]