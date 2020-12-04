import os
import json
from jinja2 import Template

class Display():
	def __init__(self, format):
		self.format = format
		self.template = None

	def build(self, data):
		if not self.format or self.format == '':
			return ''

		if self.format == 'json':
			return json.dumps(data, indent=2, sort_keys=True)

		if self.format == 'plain':
			return '\n'.join([ f'{key}: {data[key]}' for key in data ])

		template = self.from_template()
		return template.render(data)


	def from_template(self):
		if self.template:
			return self.template

		if not os.path.isfile(self.format):
			raise Exception(f"File not found: '{self.format}'")

		template = None
		with open(self.format) as f:
			template = Template(f.read())

		self.template = template
		return template

