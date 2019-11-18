from ebu_tt_live.project import description, name, version

try:
    from setuptools import setup
    extra = dict(
        include_package_data=True,
        setup_requires=['pytest-runner']
    )
except ImportError:
    from distutils.core import setup
    extra = {}


packages=[
    "ebu_tt_live",
    "ebu_tt_live.bindings",
    "ebu_tt_live.clocks",
    "ebu_tt_live.scripts",
    "ebu_tt_live.twisted",
    "ebu_tt_live.node",
    "ebu_tt_live.documents",
    "ebu_tt_live.examples"
]

setup(
    name=name,
    version=version,
    description=description,
    install_requires=[
        "PyXB",
        "ipdb>=0.10.1,<0.10.3",  # This will eventually be removed from here
        "configobj",
        "pyyaml",
        "twisted",
        "autobahn",
        "nltk",
        "sortedcontainers",
        "configman",
        "six",
        "hyperlink<17.2.0"  # This should be removed if https://github.com/python-hyper/hyperlink/issues/16 is fixed
    ],
    license="BSD3",
    packages=packages,
    package_data={
        'ebu_tt_live.examples': ['*.txt', '*.json']
    },
    entry_points={
        'console_scripts': [
            'ebu-dummy-encoder = ebu_tt_live.scripts.ebu_dummy_encoder:main',
            'ebu-interactive-shell = ebu_tt_live.scripts.ebu_interactive_shell:main',
            'ebu-simple-consumer = ebu_tt_live.scripts.ebu_simple_consumer:main',
            'ebu-simple-producer = ebu_tt_live.scripts.ebu_simple_producer:main',
            'ebu-user-input-consumer = ebu_tt_live.scripts.ebu_user_input_consumer:main',
            'ebu-user-input-forwarder = ebu_tt_live.scripts.ebu_user_input_forwarder:main',
            'ebu-ebuttd-encoder = ebu_tt_live.scripts.ebu_ebuttd_encoder:main',
            'ebu-run = ebu_tt_live.scripts.ebu_run:main'
        ]
    },
    **extra
)
