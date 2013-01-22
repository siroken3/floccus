import utils
from jinja2 import Environment, PackageLoader

def output(model):
    env = Environment(loader=PackageLoader(__name__, 'templates'), trim_blocks='True')
    env.filters['filter_only'] = utils.filter_only
    env.filters['to_cfn_tag'] = utils.to_cfn_tag
    env.filters['to_cfn_ref'] = utils.to_cfn_ref
    env.filters['to_cfn_ref_list'] = utils.to_cfn_ref_list
    env.filters['to_json_list'] = utils.to_json_list
    metatemplate = env.get_template('metatemplate.jinja2')
    return metatemplate.render(model=model)
