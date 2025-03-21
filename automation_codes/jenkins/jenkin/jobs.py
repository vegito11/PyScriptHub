import jenkins
import json
from ..utilities import get_config_var, get_job_config

class JenkinsJob(object):
	
	secret_filepath = "configs/secrets.json"
	job_section = "jenkins_jobs"
	tmpl_path = "templates"

	def __init__(self, jen_conn):
		self.jenConn = jen_conn
		
	def get_job(self, jobname="sample_app-ci"):
		# job = jen_conn.get_job_info(jobname)
		jobxml = self.jenConn.get_job_config(jobname)
		return jobxml

	def create_multibranch_job(self, jobname="sample_app"):
		
		common = get_config_var(self.secret_filepath, self.job_section, "jobconfig")
		job = get_config_var(self.secret_filepath, self.job_section, jobname)

		tmpl_filepath = f"{self.tmpl_path}/{common['template']}"
		job_xml = get_job_config(tmpl_filepath, common, job)
		
		self.jenConn.create_job(f"{jobname}-ci", job_xml)
		print(f" created the {jobname}-ci job !!!")

	def update_multibranch_job(self, jobname):
		
		common = get_config_var(self.secret_filepath, self.job_section, "jobconfig")
		job = get_config_var(self.secret_filepath, self.job_section, jobname)

		tmpl_filepath = f"{self.tmpl_path}/{common['template']}"
		updated_xml = get_job_config(tmpl_filepath, common, job)	
		self.jenConn.reconfig_job(f"{jobname}-ci", updated_xml)

		print(f" Updated the {jobname}-ci job !!!")

	def create_job(self, jobname):
		
		job = get_config_var(self.secret_filepath, self.job_section, jobname)
		tmpl_filepath = f"{self.tmpl_path}/{job['template']}"
		job_xml = get_job_config(tmpl_filepath, {}, job)

		self.jenConn.create_job(job['name'], job_xml)		
		print(f" created the {job['name']} job !!!")

	def delete_job(self, jobname):

		self.jenConn.delete_job(jobname)	
		print(f" Delete the {job['name']} job !!!")