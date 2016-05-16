
try:
    from setuptools import setup
    extra = dict(test_suite="tests.test.suite", include_package_data=True, test_requires=[])
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
    "ebu_tt_live.example_data"
]


setup(
    name="ebu-tt-live",
    version="0.0.1",
    description="EBU-TT Part 3 library implementing Specification EBU-3370",
    install_requires=[
        "PyXB",
        "ipdb",  # This will eventually be removed from here
        "configobj",
        "pyyaml",
        "twisted",
        "autobahn",
        "nltk"
    ],
    license="BSD3",
    packages=packages,
    package_data={
        'ebu_tt_live.example_data': ['*.txt']
    },
    entry_points={
        'console_scripts': [
            'ebu-dummy-encoder = ebu_tt_live.scripts.ebu_dummy_encoder:main',
            'ebu-interactive-shell = ebu_tt_live.scripts.ebu_interactive_shell:main',
            'ebu-simple-consumer = ebu_tt_live.scripts.ebu_simple_consumer:main',
            'ebu-simple-producer = ebu_tt_live.scripts.ebu_simple_producer:main'
        ]
    }
)
