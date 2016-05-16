from pkg_resources import ResourceManager, get_provider


def get_example_data(dataset_name):
    """
    This is a smart package loader that locates text files inside our package
    :param dataset_name:
    :return:
    """
    provider = get_provider('ebu_tt_live')
    manager = ResourceManager()

    source = provider.get_resource_string(manager, 'example_data/'+dataset_name)

    return source
