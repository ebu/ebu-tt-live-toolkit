from importlib.resources import read_text

current_module = __import__(__name__)


def get_example_data(dataset_name):
    """
    This is a smart package loader that locates text files inside our package
    :param dataset_name:
    :return:
    """

    source = read_text(current_module, dataset_name)

    return source
