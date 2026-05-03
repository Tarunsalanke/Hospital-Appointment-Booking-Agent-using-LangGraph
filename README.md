# Hospital Agent

A hospital agent project.

.venv/Scripts/activate

docker run -d --name hospital-redis -p 6379:6379 redis

uvicorn app.main:app --reload

streamlit run frontend/dashboard.py

docker run --rm -it postgres psql "postgresql://neondb_owner:npg_7nb0cqvEukNI@ep-cool-surf-an2mq86c-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"