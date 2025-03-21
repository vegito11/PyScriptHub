## 1) Function uses 

1. Get Jenkins Connection Object
```python
	secret_filepath = "../configs/secrets.json"
	# config_filepath = "../configs/vars.json"
	JENKINS_URL = get_config_var(secret_filepath, "jenkins", "url")
	username = get_config_var(secret_filepath, "jenkins", "username")
	password = get_config_var(secret_filepath, "jenkins", "password")
	jen_conn = get_conn(JENKINS_URL, username, password)
```

2. Create Multibranch Job
```python
	create_multibranch_job(jen_conn, "sample_app")
```
3. Get Job XML config

```python
data = get_job(jen_conn, "test-ci")
print(data)
```

4. Update the Multibranch pipeline job
```python
update_multibranch_job(jen_conn, "test")
```

## 2. Run Script:
```bash
export PYTHONPATH=$(pwd)
python main.py
python jenkin/roles.py
python jenkin/rbac.py
```

## Reference

1. https://python-jenkins.readthedocs.io/en/latest/api.html
2. https://javadoc.jenkins.io/plugin/role-strategy/com/michelin/cio/hudson/plugins/rolestrategy/RoleBasedAuthorizationStrategy.html#doAddRole-java.lang.String-java.lang.String-java.lang.String-java.lang.String-java.lang.String-