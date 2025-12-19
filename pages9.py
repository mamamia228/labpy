# рендер страниц через Jinja2

class PagesController:
    def __init__(self, env):
        self.env = env

    def render(self, tpl_name, **ctx):
        tpl = self.env.get_template(tpl_name)
        return tpl.render(**ctx).encode("utf-8")
