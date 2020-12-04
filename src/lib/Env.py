import yaml

# Env reader class
class Env():
	def __init__(self, filters=None):
		self.config_file = 'config/envs.yaml'
		self.index = -1
		self.parse()
		self.load(filters)

	def parse(self):
		with open(self.config_file) as f:
			self.config = yaml.safe_load(f.read())

	# Load the filtered env conf
	def load(self, filters=None):
		self.loaded = []
		for env in self.config:
			if 'inventory' not in env:
				env['inventory'] = env['label']
			# host = env.get('label')
			# name = env.get('name_format')
			# region = env.get('region')
			# inventory = env.get('inventory', host)

			# Filter
			skip = False
			if filters is not None:
				if any(f in env and env[f] != filters[f] for f in filters):
					continue

			self.loaded.append(env)

	# Get the next item in the config
	def next(self):
		self.index += 1
		if self.index >= len(self.loaded):
			self.index -= 1

		return self.loaded[self.index]

	# Return the previous item in the env conf
	def prev(self):
		self.index -= 1
		if self.index < 0:
			self.index = 0

		return self.loaded[self.index]

	# True if we're at the end of the env list
	def at_end(self):
		return self.index + 1 == len(self.loaded)
