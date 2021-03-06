wrk.method = "POST"
--wrk.body   = "amount=1"
--wrk.headers["Content-Type"] = "application/x-www-form-urlencoded"
wrk.body = '{"amount": "1"}'
wrk.headers["Content-Type"] = "application/json"
