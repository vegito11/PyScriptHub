import json
import os
from jinja2 import Template

def get_config_var(filepath, section, varname=None, envname=None):
	with open(filepath) as f:
		data = json.load(f)
		if not varname:
			return data[section]
		if data[section].get(varname):
			return data[section].get(varname)
		else:
			if envname:
				return os.getenv(envname.upper())
			else:	
				return os.getenv(f'{section}_{varname}'.upper())


def get_job_config(tmpl_filepath, common, job):
    # tmpl_filepath = '../templates/multibranch_job.xml'
    with open(tmpl_filepath) as file_:
        template = Template(file_.read())
    output = template.render(common=common, job=job)
    return output

if __name__ == '__main__':
	filename = "../../configs/secrets.json"
	section = "jenkins"
	
	varname = "jobconfig"
	common = get_config_var(filename, section, varname)
	# print(common)
	
	varname = "sample_app"
	job = get_config_var(filename, section, varname)
	# print(job)

	output = get_job_config(common, job)
	print(output)