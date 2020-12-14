# Command Generator

A handy curses application for generating and displaying commands based on a config file and jinja templates.  


## How to

1. Populate `config/envs.yml` in a format like:
```yaml
- label: my-dev-server
  inventory: 'ansible-inv-name'
  category: internal
  region: eu-west-2
  name_prefix: dev-server
  multi: false
  comment: A dev server
 
- label: my-prod-server
  inventory: 'ansible-inv-name'
  category: internal
  region: eu-west-2
  name_format: prod-server
  multi: false
  comment: A prod server
```
The format is flexible, all data is simply passed to the templates.

2. Add a template, such as `config/my-command.j2`
```
label: {{label}}
region: {{region}}
multi: {{multi}}
```

3. Run: `./src/gen.py --display config/my-command.j2`


## Colors

The j2 templates also support a custom color modifier at the start of lines in the format: `!![TYPE]`.  
The full list is as follows:
- `!![INFO]` - Cyan
- `!![WARN]` - Yellow
- `!![ERROR]` - Red
- `!![SUCCESS]` - Green

