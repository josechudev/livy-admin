# livy-admin

---
Livy admin is an api + web ui for managing sessions and permissions for Apache Livy API

```
docker run -p 80:80 -it --rm -v ${PWD}:/work -w /work --entrypoint /bin/sh python:3.9-alpine

uvicorn app.main:app --port 80 --host 0.0.0.0 --reload
```