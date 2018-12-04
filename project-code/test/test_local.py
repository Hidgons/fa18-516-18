from cloudmesh_data.data.provider.local import LocalProvider
from cloudmesh_data.data.Config import Config
from cloudmesh_data.data.util.debug import myself, HEADING


def test_local_provider_list():
    HEADING(myself())
    provider = LocalProvider()
    result = provider.list(".")
    print(result)
    assert 'setup.py' in result


def test_local_list():
    HEADING(myself())
    config = Config()
    print(config)
