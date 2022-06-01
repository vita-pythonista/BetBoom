curl -XPOST http://localhost:8080/api/v1/user/registration -d '{"user": {"login": "username", "password": "******"}}'
curl -XPOST http://localhost:8080/api/v1/user/login -d '{"user": {"login": "username", "password": "******"}}'
curl -XGET http://localhost:8080/api/v1/user -H 'ssid: 0c9298d7-6f97-4e73-9ad2-6d5a5b5a1503'

curl -XPOST http://localhost:8080/api/v1/user/contact -H 'ssid: d03f3a3f-e778-4e43-b23d-c579274a4c48' -d '{
  "contact": {
      "type": "phone",
      "content": "+100"
  }
}'

curl -XDELETE http://localhost:8080/api/v1/user/contact/1 -H 'ssid: 9d60dbb2-92ae-407c-80fb-91ebbbf8c1c9'
